# TCP-Based Multithreaded Client–Server Chat Application

A feature-rich, real-time chat application built with TCP sockets, multithreading, and web technologies. This project demonstrates client-server architecture, concurrent connection handling, and modern web-based communication.

## 🌟 Features

### Core Functionality
- **Real-time messaging** with TCP socket connections
- **Multithreaded server** supporting multiple concurrent clients
- **Web-based interface** accessible via browser
- **Desktop GUI client** using Python Tkinter
- **User nickname system** with online user tracking

### Media Features
- 🎤 **Voice messaging** - Record and send audio messages (max 10 seconds)
- 📹 **Video messaging** - Record and send video messages with audio (max 15 seconds)
- 🔊 Real-time audio/video playback in chat
- 📱 Responsive web interface for mobile and desktop

### Additional Features
- User join/leave notifications
- Message timestamps
- Online users sidebar
- Modern, gradient UI design
- Connection status indicators

## 🛠️ Technologies Used

### Backend
- **Python 3.x** - Core programming language
- **Socket Programming** - TCP/IP communication
- **Threading** - Concurrent client handling
- **Flask** - Web server framework
- **Flask-SocketIO** - Real-time bidirectional communication

### Frontend
- **HTML5/CSS3** - User interface
- **JavaScript** - Client-side logic
- **Socket.IO** - WebSocket communication
- **WebRTC APIs** - Media recording (getUserMedia, MediaRecorder)

## 📁 Project Structure

```
tcp-chat-project/
│
├── server.py              # TCP server (handles desktop clients)
├── client.py              # Desktop GUI client (Tkinter)
├── web_chat.py            # Web server (Flask + SocketIO)
├── templates/
│   └── chat.html          # Web interface
└── README.md              # This file
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/tcp-chat-project.git
cd tcp-chat-project
```

### Step 2: Install Dependencies
```bash
pip install flask flask-socketio python-socketio
```

### Step 3: Run the Application

#### Option A: Web-Based Chat (Recommended)

**Terminal 1 - Start Web Server:**
```bash
python web_chat.py
```
The server will start on `http://localhost:5000`

**Access the chat:**
- Open your browser and go to `http://localhost:5000`
- Enter your nickname and start chatting!

#### Option B: Desktop Client (Tkinter GUI)

**Terminal 1 - Start TCP Server:**
```bash
python server.py
```

**Terminal 2 - Run Desktop Client:**
```bash
python client.py
```

## 🌐 Making It Publicly Accessible

To share your chat with friends over the internet, use **ngrok**:

### Step 1: Install ngrok
Download from [ngrok.com](https://ngrok.com/download)

### Step 2: Expose Your Web Server
```bash
# Start your web server first
python web_chat.py

# In a new terminal, run ngrok
ngrok http 5000
```

### Step 3: Share the Link
ngrok will provide a public URL like:
```
https://abc123.ngrok-free.app
```
Share this link with anyone - they can access your chat from anywhere!

## 💻 Usage Guide

### Web Interface

1. **Join Chat:**
   - Open the web interface
   - Enter your nickname
   - Click "Join Chat"

2. **Send Text Messages:**
   - Type in the input box
   - Press Enter or click "Send"

3. **Send Audio Messages:**
   - Click "🎤 Audio" button
   - Speak into your microphone
   - Click "Stop" when done
   - Audio automatically sends

4. **Send Video Messages:**
   - Click "📹 Video" button
   - Record your video message
   - Click "Stop" in the preview window
   - Video automatically sends with audio

5. **Leave Chat:**
   - Click the "Leave" button in the header

### Desktop Client

1. **Connect:**
   - Run `client.py`
   - Click "Connect"
   - Enter server IP (use `localhost` for local testing)
   - Enter your nickname

2. **Chat:**
   - Type messages in the input box
   - Press Enter or click "Send"

3. **Disconnect:**
   - Click "Disconnect" button

## 🏗️ Architecture

### Server Architecture
```
TCP Server (server.py)
    ├── Main Thread: Accept connections
    ├── Client Thread 1: Handle client 1
    ├── Client Thread 2: Handle client 2
    └── Client Thread N: Handle client N

Web Server (web_chat.py)
    ├── Flask HTTP Server
    ├── SocketIO WebSocket Handler
    └── Broadcast Manager
```

### Communication Flow
```
Client → Socket.IO → Flask Server → Broadcast → All Clients
```

## 🔧 Configuration

### Changing Ports

**TCP Server (server.py):**
```python
PORT = 12345  # Change this value
```

**Web Server (web_chat.py):**
```python
socketio.run(app, host='0.0.0.0', port=5000)  # Change port here
```

### Media Recording Limits

Edit in `chat.html`:
```javascript
// Audio recording timeout (milliseconds)
setTimeout(() => {
    if (isRecording) stopRecording();
}, 10000);  // 10 seconds

// Video recording timeout
setTimeout(() => {
    if (isVideoRecording) stopVideoRecording();
}, 15000);  // 15 seconds
```

## 🐛 Troubleshooting

### "Connection Refused" Error
- Ensure the server is running before connecting clients
- Check firewall settings
- Verify correct IP address and port

### Media Not Working
- Grant browser permissions for camera/microphone
- Use HTTPS or localhost (required for WebRTC)
- Check browser compatibility (Chrome/Firefox recommended)

### ngrok Issues
- Use `ngrok tcp 12345` for TCP server
- Use `ngrok http 5000` for web server
- Free tier requires reconnection after 2 hours

## 📝 Course Project Details

**Course:** Computer Networks  
**Topic:** TCP-Based Multithreaded Client–Server Framework  

### Learning Objectives Demonstrated
- ✅ TCP socket programming
- ✅ Client-server architecture
- ✅ Multithreading and concurrency
- ✅ Network protocols (TCP/IP)
- ✅ Real-time communication
- ✅ Web technologies integration

### Key Concepts
- **Socket Programming:** Low-level network communication
- **Multithreading:** Handling multiple clients simultaneously
- **Protocol Design:** Message format and handling
- **Client-Server Model:** Centralized communication architecture
- **WebSockets:** Bi-directional real-time communication

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a Computer Networks course project

## 🙏 Acknowledgments

- Flask and Socket.IO documentation
- Python threading module
- WebRTC community resources

---

**Note:** This is an educational project demonstrating TCP networking concepts. For production use, consider adding:
- User authentication
- Message encryption
- Database integration
- Better error handling
- Rate limiting
- Security measures
