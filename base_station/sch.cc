#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"

#include <fstream>
#include <iostream>
#include <vector>
#include <nlohmann/json.hpp> // external json library (lightweight, header-only)

using namespace ns3;
using json = nlohmann::json;

// Fungsi untuk membaca file rb_allocation.json
std::vector<std::vector<int>> LoadRbAllocation(const std::string& filename)
{
    std::ifstream file(filename);
    json j;
    file >> j;
    return j["rb_allocation"].get<std::vector<std::vector<int>>>();
}

int main (int argc, char *argv[])
{
    CommandLine cmd;
    cmd.Parse (argc, argv);

    // Load hasil alokasi HNNS
    std::string rbFile = "output/rb_allocation.json";
    auto rbAllocation = LoadRbAllocation(rbFile);

    // Tampilkan hasil alokasi yang dibaca (sebagai validasi awal)
    std::cout << "RB Allocation Loaded from hnns_scheduler output:" << std::endl;
    for (uint32_t user = 0; user < rbAllocation.size(); user++)
    {
        std::cout << "User " << user << ": ";
        for (uint32_t rb = 0; rb < rbAllocation[user].size(); rb++)
        {
            std::cout << rbAllocation[user][rb] << " ";
        }
        std::cout << std::endl;
    }

    // ---------- Simulasi dummy jaringan sederhana ----------
    NodeContainer nodes;
    nodes.Create (3);  // Surgeon, Base Station, Pasien

    PointToPointHelper p2p;
    p2p.SetDeviceAttribute ("DataRate", StringValue ("100Mbps"));
    p2p.SetChannelAttribute ("Delay", StringValue ("1ms"));

    NetDeviceContainer devices;
    devices = p2p.Install (nodes.Get(0), nodes.Get(1));
    devices.Add(p2p.Install (nodes.Get(1), nodes.Get(2)));

    InternetStackHelper stack;
    stack.Install (nodes);

    Ipv4AddressHelper address;
    address.SetBase ("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer interfaces = address.Assign (devices);

    // Dummy Application bisa ditambahkan disini untuk traffic testing

    Simulator::Stop (Seconds (5.0));
    Simulator::Run ();
    Simulator::Destroy ();

    return 0;
}
