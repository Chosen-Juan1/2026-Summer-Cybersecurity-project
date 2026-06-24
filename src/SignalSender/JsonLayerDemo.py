from time import sleep
from scapy.layers.inet import IP, UDP
from scapy.packet import Packet
from scapy.fields import ShortField, XByteField, IntEnumField
from scapy.sendrecv import send

class Disney(Packet):
    name = "DisneyPacket"
    fields_desc=[ ShortField("mickey",5),
                 XByteField("minnie",3) ,
                 IntEnumField("donald" , 1 ,
                      { 1: "happy", 2: "cool" , 3: "angry" } ) ]
    
packet = (IP(dst="receiver") / UDP(sport=4000, dport=5000) / Disney(mickey=10, minnie=20, donald=2))
    
while True:
    print("Sending:", packet.summary(), flush=True)
    print("mickey:", packet[Disney].mickey, flush=True)
    print("minnie:", packet[Disney].minnie, flush=True)
    print("donald:", packet[Disney].donald, flush=True)
    send(packet)
    sleep(5)