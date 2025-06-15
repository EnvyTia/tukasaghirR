# Simple network simulation for telesurgery

## Requirements:

### SURGEON NODE
```sh
pip install numpy
```
structure
```
client_surgeon.py
control/
└── control_commands.json
```

### PATIENT NODE
```sh
pip install numpy

fallocate -l 112M real_time.h264 #dummy video, linux only
fsutil file createnew real_time.h264 117440512 #dummy video, windows

#just in case u got a real one
ffmpeg -i surgery_video.mp4 -vcodec libx264 -an -f h264 real_time.h264
```
structure
```
client_pasien.py
video/
└── real_time.h264
sensor/
└── sensor_data.json
vital/
└── patient_data.hl7.json
```

### BASE STATION
```sh
sudo apt update && sudo apt install -y \
git cmake g++ python3-dev python3-pip qt5-default \
libboost-all-dev libopenmpi-dev openmpi-bin \
libsqlite3-dev libgtk-3-dev ffmpeg

pip3 install numpy tensorflow flask
```
forward port 9000 dari windows ke wsl:
```sh
ip addr #cek ip wsl

netsh interface portproxy add v4tov4 listenport=9000 listenaddress=0.0.0.0 connectport=9000 connectaddress=<IP WSL>

```

| Software                          | Keterangan                    |
| --------------------------------- | ----------------------------- |
| **WSL 2 + Ubuntu 22.04**          | Subsystem Linux di Windows    |
| **Python 3.10+**                  | Untuk semua script Python     |
| **NS-3 (latest, misal ns-3.39)**  | Simulator jaringan            |
| **Boost, OpenMPI, SQLite, CMake** | Dependency NS-3               |
| **TensorFlow, NumPy**             | Library AI untuk HNNS         |
| **FFmpeg (opsional)**             | Untuk konversi video ke H.264 |
| **pip3**                          | Python package manager        |

structure
```
telesurgery-sim/
│
├── server.py               # Server penerima data
├── hnns_scheduler.py       # Algoritma HNNS
├── datasets/               # Folder untuk menyimpan data masuk
└── ns-3/                   # Instalasi NS-3 simulator
```

## Alur:

