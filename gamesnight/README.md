# 🎮 GameNight - Real-time Multiplayer Party Games

GameNight is a production-ready web application for playing interactive mini-games with friends in real-time. Built with Vue.js 3 and FastAPI, it offers a seamless multiplayer experience with synchronized gameplay, payment integration, and guest access.

## 🚀 Features

- **5 Interactive Games**: Would You Rather, Truth or Dare, 60 Seconds, Hot Seat, Draw & Guess
- **Real-time Gameplay**: Synchronized timers and instant updates via WebSocket
- **Flexible Access**: Free users with ads, paid users without ads and guest invites
- **Theme Filtering**: Customize games with different themes (General, Funny, Deep, etc.)
- **PayPal Integration**: Secure payment processing for premium features
- **Guest Access**: Paid users can invite guests without requiring sign-up
- **Modern UI**: Beautiful, responsive design with TailwindCSS

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **Cache/Session**: Redis
- **Real-time**: Socket.IO
- **Authentication**: JWT with refresh tokens
- **Payment**: PayPal SDK

### Frontend
- **Framework**: Vue.js 3
- **Build Tool**: Vite
- **State Management**: Pinia
- **Styling**: TailwindCSS
- **Real-time**: Socket.IO Client
- **HTTP Client**: Axios

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- PayPal Developer Account

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gamesnight.git
cd gamesnight
```

2. Create environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Update the `.env` files with your configuration

4. Start the application:
```bash
docker-compose up -d
```

5. Seed the database:
```bash
docker-compose exec backend python scripts/seed_data.py
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development

See individual README files in `backend/` and `frontend/` directories for detailed setup instructions.

## 📱 Game Descriptions

### Would You Rather
Players choose between two interesting options. The majority choice is revealed after voting.
- **Duration**: 60 seconds per round
- **Players**: 2+

### Truth or Dare
Classic party game where players answer truths or complete dares.
- **Duration**: 60 seconds per turn
- **Players**: 2+

### 60 Seconds
List as many unique items as possible in a given category.
- **Duration**: 60 seconds per round
- **Players**: 2+

### Hot Seat
One player answers rapid-fire questions from all other players.
- **Duration**: 60 seconds in the hot seat
- **Players**: 3+

### Draw & Guess
One player draws while others try to guess the word.
- **Duration**: 90 seconds draw, 60 seconds guess
- **Players**: 3+

## 💰 Business Model

- **Free Users**: Access to all games with ads
- **Paid Users**: 
  - No ads
  - Ability to invite guests
  - Priority support
- **Pricing**:
  - Day Pass: $1.99
  - Monthly Pass: $9.99

## 🔒 Security Features

- JWT authentication with secure refresh tokens
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization
- No PII in logs
- GDPR/POPIA compliant

## 📊 Monitoring

- **Metrics**: Prometheus endpoint at `/metrics`
- **Logging**: Structured logging with Sentry integration
- **Health Check**: Available at `/health`

## 🚀 Deployment

### Production Checklist

1. **Environment Variables**:
   - Generate strong `SECRET_KEY`
   - Use production database credentials
   - Set `PAYPAL_MODE=live` with production PayPal credentials
   - Configure proper CORS origins

2. **Database**:
   - Use managed PostgreSQL (e.g., AWS RDS, Google Cloud SQL)
   - Enable automatic backups
   - Set up read replicas for scaling

3. **Redis**:
   - Use managed Redis (e.g., AWS ElastiCache, Redis Cloud)
   - Configure persistence for session data

4. **Application**:
   - Use Gunicorn with Uvicorn workers
   - Set up SSL/TLS with Let's Encrypt
   - Configure reverse proxy (Nginx)
   - Enable HTTP/2

5. **Monitoring**:
   - Connect Prometheus to Grafana
   - Set up alerts for critical metrics
   - Configure Sentry for error tracking

## 📝 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Vue.js team for the amazing framework
- FastAPI team for the high-performance Python framework
- All contributors and testers

---

**Note**: This is a production-ready MVP. For enterprise deployments, consider additional features like:
- Multi-language support
- Advanced analytics
- Custom branding for organizations
- Video chat integration (WebRTC)
- Tournament modes