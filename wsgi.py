from flask_socketio import SocketIO
from app import app

if __name__ == '__main__':
    SocketIO(app).run(app, cors_allowed_origins="*", debug=True)
