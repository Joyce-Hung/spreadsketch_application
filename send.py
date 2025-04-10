#!/usr/bin/env python3
#import sys
#sys.path.append('/home/p4/behavioral-model/tools')
#sys.path.append('/usr/lib/python3/dist-packages')
#sys.path.append('/usr/local/lib/python3.8/dist-packages')
from scapy.all import *
from scapy.utils import rdpcap
import sys

if len(sys.argv) < 2:
    print("Usage: ./send.py [Pcap file]")
else:
    count=0
    pkts=rdpcap(sys.argv[1])
    for pkt in pkts:
        if not pkt.haslayer(Ether):
            eth = Ether(src="08:00:00:00:01:01", dst="08:00:00:00:02:02", type=0x0800)
            pkt = eth / pkt
        sendp(pkt, iface="veth2")
        count+=1
        print(count)
