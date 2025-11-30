import datetime
import os

class MessageLogger:
    def __init__(self, log_file="logs/chat_history.txt"):
        self.log_file = log_file
        # Create logs directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
    def log_message(self, message):
        """Log message to file with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def log_user_action(self, action):
        """Log user join/leave actions"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {action}\n")
    
    def clear_log(self):
        """Clear the log file"""
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"=== Chat Session Started at {datetime.datetime.now()} ===\n")
