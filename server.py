import socket
import threading
import datetime

class ChatServer:
    def __init__(self, host='0.0.0.0', port=12345):  
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message, sender_client=None):
        """Send message to all connected clients"""
        for client in self.clients:
            if client != sender_client:
                try:
                    client.send(message)
                except:
                    self.remove_client(client)
    
    def remove_client(self, client):
        """Remove disconnected client"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            client.close()
    
    def handle_client(self, client):
        """Handle messages from client"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    formatted_message = f"[{timestamp}] {message.decode('utf-8')}".encode('utf-8')
                    self.broadcast(formatted_message, client)
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break
    
    def start_server(self):
        """Start the chat server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        
        # Show actual IP for others to connect
        import socket as sock
        hostname = sock.gethostname()
        local_ip = sock.gethostbyname(hostname)
        
        print(f"Server is listening on {self.host}:{self.port}")
        print(f"Your IP address: {local_ip}")
        print(f"Others can connect using: {local_ip}:{self.port}")
        print("Waiting for clients to connect...")
        
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            
            # Request nickname
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f"Nickname of client {address} is {nickname}")
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to server!'.encode('utf-8'))
            
            # Start handling thread for client
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()
