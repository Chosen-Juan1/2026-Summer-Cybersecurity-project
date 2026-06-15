import os
import signal
import sys


from scapy.all import sniff, IP, UDP, Raw

def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    packet.show()
    if(Raw in packet):
        print(f"Information sent with flush: {packet[Raw].load}\n", flush=True)



sniff(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp port 5000" #<- apperantly this needs a specific linux lib, added it to the docker file
)


#FIrst stage: server running with good interface on the server

#Second stage


#make sure it works on 2-3 scenarios

##Dont worry about the PS simu


##somethng that you send to the server, and the server computes smth and sends it back

#ROS: RObotic operating system

#INfo is not encrypted

#mmoduler man in the middle of man