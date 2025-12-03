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

statistics = {
    'total_messages': 0,
    'total_audio': 0,
    'total_video': 0,
    'total_users_joined': 0,
    'peak_users': 0,
    'server_start_time': datetime.datetime.now()
}

@app.route('/')
def index():
    """Main chat page"""
    return render_template('chat.html')

@app.route('/statistics')
def stats_page():
    """Statistics page"""
    return render_template('statistics.html')

@socketio.on('get_statistics')
def send_statistics():
    """Send real-time statistics to client"""
    uptime = datetime.datetime.now() - statistics['server_start_time']
    hours = int(uptime.total_seconds() // 3600)
    minutes = int((uptime.total_seconds() % 3600) // 60)
    
    stats_data = {
        'total_messages': statistics['total_messages'],
        'total_audio': statistics['total_audio'],
        'total_video': statistics['total_video'],
        'total_users': statistics['total_users_joined'],
        'active_users': len(connected_users),
        'peak_users': statistics['peak_users'],
        'uptime': f'{hours}h {minutes}m',
        'avg_msg_length': round(sum(len(msg.get('message', '')) for msg in chat_history) / max(len(chat_history), 1), 1)
    }
    emit('statistics_update', stats_data)

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

    statistics['total_users_joined'] += 1
    if len(connected_users) > statistics['peak_users']:
        statistics['peak_users'] = len(connected_users)
    
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

    statistics['total_messages'] += 1
    
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

    statistics['total_audio'] += 1
    
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

    statistics['total_video'] += 1
    
    # Broadcast video to all clients
    emit('video_message', message, broadcast=True)
    print(f'{nickname} sent a video message')

if __name__ == '__main__':
    print("=== TCP Chat Web Server ===")
    print("Server starting on http://localhost:5000")
    print("Others can connect using your IP address on port 5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
