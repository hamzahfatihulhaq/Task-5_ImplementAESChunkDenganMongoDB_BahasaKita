from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from tqdm import tqdm

from decouple import config
SECRET_KEY = config('SECRET_KEY').encode('utf-8')
BATCH_SIZE = int(1 * 1024 * 1024)
# Fungsi untuk enkripsi data menggunakan AES
async def encrypt_data(data, progress_callback):
    ciphertexts=[]
    load =0
    total = sum(len(chunk) for chunk in data )
    with tqdm(total=len(data), desc="Encrypting data", unit='B', unit_scale=True, mininterval=0.5) as pbar:
        for chunk in data:
            cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
            nonce = cipher.nonce
            # print(SECRET_KEY)
            ciphertext, tag = cipher.encrypt_and_digest(chunk)
            
            ciphertexts.append(nonce + ciphertext + tag)
            
            load += len(chunk)
            progress_callback((load/total)*100)
            # print((load/total)*100)
            
            pbar.update(len(chunk))
    
    return b''.join(ciphertexts)

# Fungsi untuk dekripsi data menggunakan AES
async def decrypt_data(data, progress_callback):
    # print(SECRET_KEY)
    plaintexts = []
    offset = 0
    chunk_size = 16 + BATCH_SIZE + 16

    with tqdm(total=len(data), desc="Decrypting data", unit='B', unit_scale=True) as pbar:
        while offset < len(data):
            chunk = data[offset:offset + chunk_size]
            nonce = chunk[:16]
            ciphertext = chunk[16:-16]
            tag = chunk[-16:]

            cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            try:
                cipher.verify(tag)
                plaintexts.append(plaintext)
                
                progress_callback((offset/len(data))*100) # Panggil callback progres
                # print((offset/len(data))*100)
            except ValueError:
                print("Key incorrect or message corrupted")

            offset += chunk_size
            pbar.update(chunk_size)  # Update progress bar with chunk size
            

    return b''.join(plaintexts)