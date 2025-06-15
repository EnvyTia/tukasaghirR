uint16_t portEmbb = 6000;
BulkSendHelper embbApp("ns3::TcpSocketFactory",
                        InetSocketAddress(interfaces.GetAddress(2), portEmbb));
embbApp.SetAttribute("MaxBytes", UintegerValue(0));  // unlimited transfer

ApplicationContainer appsEmbb = embbApp.Install(nodes.Get(0));
appsEmbb.Start(Seconds(1.0));
appsEmbb.Stop(Seconds(10.0));
