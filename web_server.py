from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import datetime
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=10000000)  # 10MB for audio

# Store connected users
connected_users = {}
chat_history = []

@app.route('/')
def index():
    """Main chat page"""
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f'Client {request.sid} connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    if request.sid in connected_users:
        nickname = connected_users[request.sid]
        del connected_users[request.sid]
        
        # Notify others
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        message = {
            'nickname': 'System',
            'message': f'{nickname} left the chat!',
            'timestamp': timestamp,
            'type': 'leave'
        }
        emit('message', message, broadcast=True)
        print(f'{nickname} disconnected')

@socketio.on('join')
def handle_join(data):
    """Handle user joining chat"""
    nickname = data['nickname']
    connected_users[request.sid] = nickname
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    message = {
        'nickname': 'System',
        'message': f'{nickname} joined the chat!',
        'timestamp': timestamp,
        'type': 'join'
    }
    
    # Send chat history to new user
    for msg in chat_history[-50:]:  # Last 50 messages
        emit('message', msg)
    
    # Notify others
    emit('message', message, broadcast=True)
    
    # Update user list
    emit('user_list', list(connected_users.values()), broadcast=True)
    print(f'{nickname} joined the chat')

@socketio.on('send_message')
def handle_message(data):
    """Handle chat message"""
    nickname = connected_users.get(request.sid, 'Unknown')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    message = {
        'nickname': nickname,
        'message': data['message'],
        'timestamp': timestamp,
        'type': 'message'
    }
    
    # Store in history
    chat_history.append(message)
    
    # Broadcast to all clients
    emit('message', message, broadcast=True)
    print(f'{nickname}: {data["message"]}')

@socketio.on('send_audio')
def handle_audio_message(data):
    """Handle audio message"""
    nickname = connected_users.get(request.sid, 'Unknown')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    message = {
        'nickname': nickname,
        'audio': data['audio'],
        'timestamp': timestamp,
        'type': 'audio'
    }
    
    # Broadcast audio to all clients
    emit('audio_message', message, broadcast=True)
    print(f'{nickname} sent an audio message')

@socketio.on('send_video')
def handle_video_message(data):
    """Handle video message"""
    nickname = connected_users.get(request.sid, 'Unknown')
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    message = {
        'nickname': nickname,
        'video': data['video'],
        'timestamp': timestamp,
        'type': 'video'
    }
    
    # Broadcast video to all clients
    emit('video_message', message, broadcast=True)
    print(f'{nickname} sent a video message')

if __name__ == '__main__':
    print("=== TCP Chat Web Server ===")
    print("Server starting on http://localhost:5000")
    print("Others can connect using your IP address on port 5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
