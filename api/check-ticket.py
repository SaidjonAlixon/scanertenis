from http.server import BaseHTTPRequestHandler
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import pytz

# Timezone
UZBEKISTAN_TZ = pytz.timezone('Asia/Tashkent')

def get_uzbekistan_time():
    """O'zbekiston vaqtini olish"""
    return datetime.now(UZBEKISTAN_TZ)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # CORS headers
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Request body ni o'qish
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            ticket_id = data.get('ticket_id')
            if not ticket_id:
                response = {'error': 'Ticket ID kiritilmagan'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Database connection
            database_url = os.environ.get('DATABASE_URL')
            if not database_url:
                response = {'error': 'Database sozlanmagan'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Ticket ma'lumotlarini olish
            cursor.execute("""
                SELECT b.*, u.full_name, u.phone, c.name as court_name, t.consumed_at
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                JOIN courts c ON b.court_id = c.id
                LEFT JOIN tickets t ON b.id = t.booking_id
                WHERE b.ticket_id = %s
            """, (ticket_id,))
            
            booking = cursor.fetchone()
            
            if not booking:
                response = {
                    'status': 'invalid',
                    'message': 'Ticket topilmadi'
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Vaqtni tekshirish
            current_time = get_uzbekistan_time()
            booking_date = booking['date']
            booking_end_time = booking['end_time']
            
            # Booking yakunlanish vaqtini hisoblash
            booking_end_datetime = datetime.combine(booking_date, 
                datetime.strptime(booking_end_time, '%H:%M').time())
            booking_end_datetime = UZBEKISTAN_TZ.localize(booking_end_datetime)
            
            # Ticket ishlatilganligini tekshirish
            if booking['consumed_at']:
                response = {
                    'status': 'used',
                    'message': 'Ticket allaqachon ishlatilgan',
                    'consumed_at': booking['consumed_at'].isoformat()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Muddati o'tganligini tekshirish
            if current_time > booking_end_datetime:
                response = {
                    'status': 'expired',
                    'message': 'Ticket muddati tugagan',
                    'expired_at': booking_end_datetime.isoformat()
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
                return
            
            # Haqiqiy ticket
            response = {
                'status': 'valid',
                'message': 'Ticket haqiqiy',
                'ticket_id': ticket_id,
                'customer_name': booking['full_name'],
                'phone': booking['phone'],
                'court_name': booking['court_name'],
                'date': booking['date'].isoformat(),
                'start_time': booking['start_time'],
                'end_time': booking['end_time'],
                'amount': float(booking['amount'])
            }
            
            cursor.close()
            conn.close()
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {'error': str(e)}
            self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
