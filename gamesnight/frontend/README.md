# GameNight Frontend

Vue.js 3 frontend for the GameNight web application.

## Features

- Vue 3 with Composition API
- Vite for fast development
- Pinia for state management
- TailwindCSS for styling
- Socket.IO for real-time communication
- PayPal integration for payments

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Copy the example environment file:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
   - `VITE_API_URL`: Backend API URL
   - `VITE_WS_URL`: WebSocket URL
   - `VITE_PAYPAL_CLIENT_ID`: PayPal client ID (optional for development)

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── assets/         # Static assets
├── components/     # Reusable Vue components
│   └── games/      # Game-specific components
├── router/         # Vue Router configuration
├── services/       # API and WebSocket services
├── stores/         # Pinia stores
├── views/          # Page components
└── main.js         # Application entry point
```

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

### Key Components

#### Stores (Pinia)
- `auth` - User authentication state
- `room` - Game room management
- `game` - Active game state

#### Services
- `api.js` - HTTP requests with Axios
- `websocket.js` - Real-time communication

#### Views
- `Home` - Landing page
- `Login/Register` - Authentication
- `Dashboard` - User dashboard
- `CreateRoom` - Room creation
- `GameRoom` - Active game interface
- `Subscription` - Payment handling

## Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

## Deployment

### Using Nginx

1. Build the application
2. Copy `dist/` contents to your web server
3. Configure Nginx for SPA routing (see `nginx.conf`)

### Using Docker

```bash
docker build -t gamesnight-frontend .
docker run -p 80:80 gamesnight-frontend
```

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)
- `VITE_WS_URL` - WebSocket URL (default: ws://localhost:8000)
- `VITE_PAYPAL_CLIENT_ID` - PayPal Client ID for payments

## Contributing

1. Follow Vue 3 style guide
2. Use Composition API for new components
3. Maintain consistent styling with TailwindCSS
4. Add appropriate TypeScript types (future enhancement)
