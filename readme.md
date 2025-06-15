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

## Base station guide

```sh
#  setelah installasi ns-3
cd ~/ns-3
mkdir external
cd external
git clone https://github.com/nlohmann/json.git
```
update 
```sh
nano ~/ns-3/CMakeLists.txt
# Tambahkan external include path:

# Include external JSON
include_directories(${CMAKE_SOURCE_DIR}/external/json/include)

# Tambahkan scratch file spesifik
add_executable(hnns-schedular-sim scratch/hnns-schedular-sim.cc)

# Link dengan module NS-3 modern
target_link_libraries(hnns-schedular-sim
    ns3::core
    ns3::internet
    ns3::network
    ns3::point-to-point
    ns3::applications
    ns3::flow-monitor
)


# update pada bagian 
target_link_libraries(hnns-schedular-sim
    ns3::core
    ns3::internet
    ns3::network
    ns3::point-to-point
    ns3::applications
    ns3::flow-monitor
)


```

buat kode simulasi
```sh
cd ~/ns-3/scratch
nano hnns-scheduler-sim.cc
```
dengan isi file 
```cpp
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-helper.h"

#include <fstream>
#include <nlohmann/json.hpp>

using namespace ns3;
using json = nlohmann::json;

// Fungsi membaca file RB allocation hasil HNNS
std::vector<std::vector<int>> LoadRbAllocation(const std::string& filename)
{
    std::ifstream file(filename);
    json j;
    file >> j;
    return j["rb_allocation"].get<std::vector<std::vector<int>>>();
}

NS_LOG_COMPONENT_DEFINE ("HnnsSchedulerSimulation");

int main (int argc, char *argv[])
{
    CommandLine cmd;
    cmd.Parse(argc, argv);

    // Load file rb_allocation.json hasil hnns_scheduler.py
    auto rbAllocation = LoadRbAllocation("output/rb_allocation.json");

    std::cout << "Loaded RB Allocation:" << std::endl;
    for (size_t u = 0; u < rbAllocation.size(); ++u)
    {
        std::cout << "User " << u << ": ";
        for (size_t rb = 0; rb < rbAllocation[u].size(); ++rb)
            std::cout << rbAllocation[u][rb] << " ";
        std::cout << std::endl;
    }

    // Membuat dummy topologi 3 node
    NodeContainer nodes;
    nodes.Create(3);

    PointToPointHelper p2p;
    p2p.SetDeviceAttribute("DataRate", StringValue("100Mbps"));
    p2p.SetChannelAttribute("Delay", StringValue("1ms"));

    NetDeviceContainer d1 = p2p.Install(nodes.Get(0), nodes.Get(1));
    NetDeviceContainer d2 = p2p.Install(nodes.Get(1), nodes.Get(2));

    InternetStackHelper stack;
    stack.Install(nodes);

    Ipv4AddressHelper address;
    address.SetBase("10.1.1.0", "255.255.255.0");
    address.Assign(d1);
    address.SetBase("10.1.2.0", "255.255.255.0");
    address.Assign(d2);

    // Membuat traffic URLLC dummy
    uint16_t portUrlLc = 5000;
    OnOffHelper urlccApp("ns3::UdpSocketFactory",
                         InetSocketAddress("10.1.2.2", portUrlLc));
    urlccApp.SetAttribute("DataRate", StringValue("2Mbps"));
    urlccApp.SetAttribute("PacketSize", UintegerValue(200));

    urlccApp.Install(nodes.Get(0))->Start(Seconds(1.0));
    urlccApp.Install(nodes.Get(0))->Stop(Seconds(10.0));

    // Membuat traffic eMBB dummy
    uint16_t portEmbb = 6000;
    BulkSendHelper embbApp("ns3::TcpSocketFactory",
                            InetSocketAddress("10.1.2.2", portEmbb));
    embbApp.SetAttribute("MaxBytes", UintegerValue(0));

    embbApp.Install(nodes.Get(0))->Start(Seconds(1.0));
    embbApp.Install(nodes.Get(0))->Stop(Seconds(10.0));

    // Monitoring flow untuk hasil pengujian
    FlowMonitorHelper flowmon;
    Ptr<FlowMonitor> monitor = flowmon.InstallAll();

    Simulator::Stop(Seconds(12.0));
    Simulator::Run();

    monitor->SerializeToXmlFile("flowmon-results.xml", true, true);
    Simulator::Destroy();

    return 0;
}
```

build ulang
```sh
# just in case
rm -rf *
#############
cd ~/ns-3/build
cmake ..
cmake --build .
```

run simulasi
```sh
./ns3 run scratch/hnns-scheduler-sim
```

parser flowmon
```sh
python3 parse_flowmon.py
```
