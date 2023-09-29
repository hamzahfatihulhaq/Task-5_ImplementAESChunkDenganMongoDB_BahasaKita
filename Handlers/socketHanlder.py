from tornado.websocket import WebSocketHandler
import uuid
progress_ws_instances = set()

class ProgressWebSocket(WebSocketHandler):
    instances = set()

    def open(self):
        self.progress = 0  # Inisialisasi nilai progres
        self.progress_increment = 0  # Inisialisasi increment progres
        self.id = uuid.uuid4().hex  # Buat ID unik
        ProgressWebSocket.instances.add(self)
        self.write_message({"message": "WebSocket connection established"})

    def on_close(self):
        ProgressWebSocket.instances.remove(self)

    def on_message(self, message):
        self.write_message(message)

    def send_progress(self, progress):
        self.progress = progress
        self.write_message({"progress": f"{self.progress:.2f}%", "message": "Proses Loading"})

    def send_complete(self):
        self.write_message({"message": "Proses selesai"})
        
