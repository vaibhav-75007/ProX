import threading
import json

class Server:
    def __init__(self, IPAddress, Port, DBPath):
        self.IPAddress = IPAddress  # Server's IP address
        self.Port = Port  # Server's port
        self.DBPath = DBPath  # Path to the JSON file containing the app's database
        self.IdleTimer = 0  # Timer to unload data from memory

        # Dictionaries containing classes' data from the main app. Key: unique id, value: json-like dicts containing data
        self.Users = dict()
        self.Tasks = dict()
        self.Flashcards = dict()

    def run(self):
        """Start the server. Wait for request. Count idle time"""
        pass
    
    def load_db(self):
        """Load up the database from file into memory"""
        pass

    def update_db(self, **kwargs):
        """Update a field"""
        pass

    def unload_db(self):
        """Save the database to JSON and unload it from memory"""
        pass

    def count_idle_time(self, timeout):
        """Increase IdleTimer every second"""
        pass

    def add_user(self):
        """Add user from the database into Users dict"""
        pass

    def add_task(self):
        """Add task from the database into Tasks dict"""
        pass

    def add_flashcard(self):
        """Add flashcard from the database into Flashcards dict"""
        pass

    def parse_request(self, message):
        """Treat the request message accordingly"""
        pass

    def compose_response(self, **kwargs):
        """Compose a response to be sent to client. Returns the composed message"""
        pass

    def respond(self, message):
        """Send back the response message"""
        pass