import socket

# -------------------------------
# KONFIGURASI SERVER
# -------------------------------

BASE_STATION_IP = "192.168.1.100"  # Ganti IP BS
PORT = 9000

# -------------------------------
# FUNGSI PENGIRIMAN DATA
# -------------------------------

def send_file(file_path, header):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BASE_STATION_IP, PORT))
        s.sendall(header.ljust(64).encode())  # kirim header fixed 64 byte

        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                s.sendall(chunk)
    print(f"[INFO] Data {header} berhasil dikirim.")

# -------------------------------
# PENGIRIMAN DATA KONTROL ROBOTIK
# -------------------------------

if __name__ == "__main__":
    # Kirim file kontrol robotik
    send_file("control/control_commands.json", "kontrol")

    print("[CLIENT SURGEON] Data kontrol berhasil dikirim.")
