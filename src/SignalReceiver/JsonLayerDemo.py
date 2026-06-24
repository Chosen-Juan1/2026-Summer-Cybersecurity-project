from time import sleep
from scapy.layers.inet import IP, UDP
from scapy.packet import Packet, bind_layers
from scapy.fields import ShortField, XByteField, IntEnumField
from scapy.sendrecv import sniff

class Disney(Packet):
    name = "DisneyPacket"
    fields_desc=[ ShortField("mickey",5),
                 XByteField("minnie",3) ,
                 IntEnumField("donald" , 1 ,
                      { 1: "happy", 2: "cool" , 3: "angry" } ) ]

bind_layers(UDP, Disney, dport=5000)

def sniffer_callback(packet: Packet):
    print("Received:", packet.summary(), flush=True)
    print(packet[Disney].mickey, flush=True)
    print(packet[Disney].minnie, flush=True)
    print(packet[Disney].donald, flush=True)

sniff(
    prn=sniffer_callback,
    filter="udp port 5000"
)