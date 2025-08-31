# 🎾 Tennis QR Scanner - Vercel Deployment

Tennis Court QR Scanner web application for Vercel deployment.

## 🚀 Features

- **📱 QR Code Scanning**: Camera-based QR code scanning
- **📝 Manual Input**: Manual ticket ID verification
- **🔍 Real-time Verification**: Live ticket validation
- **⏰ Timezone Support**: Asia/Tashkent timezone
- **📱 Mobile Responsive**: Works on all devices
- **🔒 Secure API**: PostgreSQL backend

## 📁 File Structure

```
qr-scanner-vercel/
├── index.html          # Main QR scanner interface
├── api/
│   └── check-ticket.py # Serverless API function
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── package.json        # Node.js configuration
└── README.md          # This file
```

## 🌐 Deploy to Vercel

### 1. Install Vercel CLI
```bash
npm install -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy
```bash
cd qr-scanner-vercel
vercel
```

### 4. Set Environment Variables
In Vercel dashboard, add:
```env
DATABASE_URL=your_postgresql_connection_string
```

### 5. Production Deploy
```bash
vercel --prod
```

## 🔧 Environment Variables

Required in Vercel dashboard:

- `DATABASE_URL`: PostgreSQL connection string from Railway

## 🔗 API Endpoints

- `GET /`: QR Scanner web interface
- `POST /api/check-ticket`: Ticket verification API

## 📱 Usage

1. Open the deployed URL in browser
2. Allow camera permission
3. Point camera at QR code
4. Or manually enter ticket ID
5. View verification result

## 🛠️ Development

```bash
# Local development
vercel dev

# Test API
curl -X POST http://localhost:3000/api/check-ticket \
  -H "Content-Type: application/json" \
  -d '{"ticket_id": "TICKET123"}'
```

## 🔒 Security

- CORS enabled for all origins
- Input validation
- SQL injection protection
- Real-time ticket validation

## 📊 Response Format

### Valid Ticket
```json
{
  "status": "valid",
  "message": "Ticket haqiqiy",
  "ticket_id": "TICKET123",
  "customer_name": "John Doe",
  "phone": "+998901234567",
  "court_name": "Kort 1",
  "date": "2025-01-15",
  "start_time": "10:00",
  "end_time": "11:00",
  "amount": 100000
}
```

### Expired Ticket
```json
{
  "status": "expired",
  "message": "Ticket muddati tugagan",
  "expired_at": "2025-01-15T11:00:00+05:00"
}
```

### Used Ticket
```json
{
  "status": "used",
  "message": "Ticket allaqachon ishlatilgan",
  "consumed_at": "2025-01-15T10:30:00+05:00"
}
```

### Invalid Ticket
```json
{
  "status": "invalid",
  "message": "Ticket topilmadi"
}
```

---

**🎾 Tennis QR Scanner - Powered by Vercel**
