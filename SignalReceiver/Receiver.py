import os
import signal
import sys


from scapy.all import sniff, IP, UDP, Raw

def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    if(Raw in packet):
        packet.show()
        print(f"Information sent: {packet[Raw].load}\n")
        print(f"Information sent: {packet[Raw].load}\n", flush=True)



sniff(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp port 5000" #<- apperantly this needs a specific linux lib, added it to the docker file
)
