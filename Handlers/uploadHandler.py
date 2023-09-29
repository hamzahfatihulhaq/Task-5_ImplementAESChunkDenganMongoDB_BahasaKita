import os
import tornado.web
import uuid
from AES_utils import decrypt_data,encrypt_data
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Handlers.socketHanlder import ProgressWebSocket

class UploadHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            uploaded_file = self.request.files['file'][0]
            file_content = uploaded_file['body']
            # Membuat ID unik
            unique_id = self.create_unique_id()

            print("sukses")
            # Enkripsi file
            # decrypted_data = await decrypt_data(file_content)
            
            # Inisialisasi progres WebSocket
            def progress_callback(progress):
                for instance in ProgressWebSocket.instances:
                    instance.send_progress(progress)

            decrypted_data = await decrypt_data(file_content, progress_callback)

            for instance in ProgressWebSocket.instances:
                instance.send_complete()
            # Simpan file terenkripsi
            decrypted_filename = os.path.join("Uploads", unique_id)
            with open(decrypted_filename, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            self.write({"message": "Proses selesai"})

        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})

    def create_unique_id(self):
        # Kode untuk membuat ID unik di sini, misalnya dengan modul uuid
        unique_id = str(uuid.uuid4())  # Membuat UUID versi 4 (random)
        return unique_id
    