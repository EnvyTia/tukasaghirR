FlowMonitorHelper flowmon;
Ptr<FlowMonitor> monitor = flowmon.InstallAll();

Simulator::Stop(Seconds(10.0));
Simulator::Run();

monitor->SerializeToXmlFile("flowmon-results.xml", true, true);
Simulator::Destroy();
