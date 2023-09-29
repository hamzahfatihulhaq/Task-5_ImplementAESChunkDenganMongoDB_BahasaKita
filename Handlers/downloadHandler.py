import os
import tornado.web
from AES_utils import decrypt_data,encrypt_data
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Handlers.socketHanlder import ProgressWebSocket

BATCH_SIZE = int(1 * 1024 * 1024)

class DownloadHandler(tornado.web.RequestHandler):
    async def get(self, filename):
        # Lakukan pengecekan id di sini, misalnya dari database atau sesuai logika aplikasi Anda
        valid_id = self.check_id_validity(filename)  # Gantilah ini dengan logika validasi yang sesuai
        print(valid_id)
        if valid_id:
            # Baca file terenkripsi
            decrypted_filename = os.path.join("Uploads", filename)
            chunks=[]
            with open(decrypted_filename, "rb") as decrypted_file:
                while True:
                    decrypted_data = decrypted_file.read(BATCH_SIZE)
                    if not decrypted_data:
                        break
                    chunks.append(decrypted_data)

            # Dekripsi file
            def progress_callback(progress):
                for instance in ProgressWebSocket.instances:
                    instance.send_progress(progress)

            encrypted_data = await encrypt_data(chunks, progress_callback)

            for instance in ProgressWebSocket.instances:
                instance.send_complete()

            # Set header agar browser mengenali kontennya sebagai file
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', f'attachment; filename={filename}')
            
            # Kirim data terdekripsi ke browser
            self.write(encrypted_data)
        
        else:
            self.set_status(404)
            self.write({"error": "File not found"})  # Gantilah pesan kesalahan ini sesuai kebutuhan

    def check_id_validity(self, filename):
        for file in os.listdir("Uploads"):
            if file.startswith(filename):
                return True
        
        return False