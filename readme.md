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

cd ns-3
mkdir external
cd external
git clone https://github.com/nlohmann/json.git

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

on BS
```sh
wsl --install -d Ubuntu-22.04
sudo apt update && sudo apt upgrade -y
sudo apt install git cmake g++ python3-dev python3-pip qt5-default \
libboost-all-dev libopenmpi-dev openmpi-bin \
libsqlite3-dev libgtk-3-dev ffmpeg
pip3 install numpy tensorflow flask

# run the one in base station
cd ~
git clone https://gitlab.com/nsnam/ns-3-dev.git ns-3
cd ns-3
./ns3 configure --enable-examples --enable-tests
./ns3 build

mkdir external && cd external
git clone https://github.com/nlohmann/json.git

cd ~/ns-3/scratch

nano hnns-scheduler-sim.cc

# paste

cd ~/ns-3
./ns3 build
./ns3 run scratch/hnns-scheduler-sim

# buka wscript di root
def configure(conf):
    conf.env.append_value('CXXFLAGS', '-std=c++17')
    conf.env.append_value('CXXFLAGS', '-Iexternal/json/include')

```

schedular
```sh
cd ~/ns-3/src/lte/model
cp pf-ff-mac-scheduler.cc hnns-mac-scheduler.cc
cp pf-ff-mac-scheduler.h hnns-mac-scheduler.h

ubah class PfFfMacScheduler : public FfMacScheduler
jadi class HnnsMacScheduler : public FfMacScheduler

```

```sh 
# override fungsi
void DoSchedDlTriggerReq (const FfMacSchedSapProvider::SchedDlTriggerReqParameters& params);
# Ini fungsi utama NS-3 yang setiap 1 TTI (Transmission Time Interval) memutuskan RB allocation.

#copy scheduler bawaan
cd ~/ns-3/src/lte/model
cp pf-ff-mac-scheduler.cc hnns-mac-scheduler.cc
cp pf-ff-mac-scheduler.h hnns-mac-scheduler.h
# rename class dalam file
class PfFfMacScheduler : public FfMacScheduler
class HnnsMacScheduler : public FfMacScheduler

```