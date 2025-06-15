uint16_t portUrlLc = 5000;
OnOffHelper urlccApp("ns3::UdpSocketFactory",
                     InetSocketAddress(interfaces.GetAddress(1), portUrlLc));
urlccApp.SetAttribute("DataRate", StringValue("2Mbps"));
urlccApp.SetAttribute("PacketSize", UintegerValue(200));  // kecil, low-latency
urlccApp.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
urlccApp.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));

ApplicationContainer appsUrlLc = urlccApp.Install(nodes.Get(0));
appsUrlLc.Start(Seconds(1.0));
appsUrlLc.Stop(Seconds(10.0));
