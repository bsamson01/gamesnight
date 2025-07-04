# GameNight Backend

FastAPI backend for the GameNight web application.

## Features

- JWT-based authentication with refresh tokens
- Real-time game communication via Socket.IO
- PostgreSQL for data persistence
- Redis for session management and caching
- PayPal integration for payments
- 5 mini-games with synchronized gameplay

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- PayPal Developer Account (for payments)

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the example environment file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
   - Database credentials
   - Redis URL
   - Secret key for JWT
   - PayPal credentials

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
app/
├── api/           # API endpoints
├── core/          # Core configurations
├── db/            # Database configuration
├── models/        # SQLAlchemy models
├── schemas/       # Pydantic schemas
├── services/      # Business logic
└── websocket/     # Socket.IO configuration
```

## WebSocket Events

### Client → Server
- `connect`: Authenticate and connect
- `join_room`: Join a game room
- `leave_room`: Leave a game room
- `game_action`: Send game actions
- `start_timer`: Start synchronized timer
- `drawing_stroke`: Send drawing data

### Server → Client
- `connected`: Connection confirmed
- `user_joined`: User joined room
- `user_left`: User left room
- `game_update`: Game state update
- `timer_sync`: Timer synchronization
- `stroke_update`: Drawing update

## Testing

Run tests with:
```bash
pytest
```

## Production Deployment

1. Use production database and Redis
2. Set `PAYPAL_MODE=live` with production PayPal credentials
3. Configure proper CORS origins
4. Set up SSL/TLS
5. Use a process manager like Gunicorn
6. Set up monitoring with Prometheus/Grafana