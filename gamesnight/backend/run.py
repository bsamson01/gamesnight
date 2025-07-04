import uvicorn
import socketio
from app.main import app
from app.websocket.socketio_app import sio

# Create a combined ASGI app
combined_app = socketio.ASGIApp(sio, app)

if __name__ == "__main__":
    uvicorn.run(
        "run:combined_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )