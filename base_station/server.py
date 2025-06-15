import socket
import threading
import os
from datetime import datetime

# -------------------------------
# KONFIGURASI
# -------------------------------

HOST = "0.0.0.0"
PORT = 9000  # Port default untuk komunikasi

DATASET_DIR = "datasets"
os.makedirs(DATASET_DIR, exist_ok=True)

# -------------------------------
# HANDLER UNTUK SETIAP KONEKSI MASUK
# -------------------------------

def handle_client(conn, addr):
    print(f"[INFO] Koneksi dari {addr}")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Baca header data (misalnya jenis: video, sensor, vital, kontrol)
    header = conn.recv(64).decode().strip()
    filename = f"{header}_{timestamp}.bin"

    filepath = os.path.join(DATASET_DIR, filename)
    with open(filepath, "wb") as f:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)

    print(f"[DATA] Data '{header}' dari {addr} disimpan ke: {filepath}")
    conn.close()

# -------------------------------
# MAIN SERVER
# -------------------------------

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER] Menunggu koneksi di {HOST}:{PORT}...")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
