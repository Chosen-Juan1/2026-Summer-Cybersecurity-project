from time import sleep
from scapy.fields import IntEnumField, ShortField, XByteField
from scapy.layers.inet import IP, UDP
from scapy.packet import Packet
from scapy.sendrecv import sniff
from TheManInTheMiddle.ApplyAndSend import apply_and_send
from Attacks.FieldModification import modify_field
from Utils.protocol_serialization import bind_protocol

bind_protocol([("IP", False), ("UDP", False), ("DisneyPacket", True)], {"DisneyPacket": 
'''
{
    "name": "DisneyPacket",
    "fields_desc": [
        {"name": "mickey", "default": 5, "fmt": "H"},
        {"name": "minnie", "default": 3, "fmt": "B"}
    ],
    "enum_fields_desc": [
        {"name": "donald", "default": 1, "enum": {"1": "happy", "2": "cool", "3": "angry"}, "fmt": "I"}
    ]
}
'''})

def modify_packet(packet):
    if packet.haslayer("DisneyPacket"):
        disney_layer = packet.getlayer("DisneyPacket")
        disney_layer.mickey = 99
        disney_layer.minnie = 99
        disney_layer.donald = 3
    return packet

def demo_modify_packet():
    class Disney(Packet):
        name = "DisneyPacket"
        fields_desc=[ ShortField("mickey",5),
                    XByteField("minnie",3) ,
                    IntEnumField("donald" , 1 ,
                        { 1: "happy", 2: "cool" , 3: "angry" } ) ]
    packet = (IP(dst="1.1.1.1") / UDP(sport=4000, dport=5000) / Disney(mickey=10, minnie=20, donald=2))
    print("Original packet:", packet.summary())
    print(packet[Disney].mickey, packet[Disney].minnie, packet[Disney].donald)
    modified_packet = modify_packet(packet)
    print("Modified packet:", modified_packet.summary())
    print(modified_packet[Disney].mickey, modified_packet[Disney].minnie, modified_packet[Disney].donald)

sleep(2)
sniff(
    prn=lambda x: apply_and_send(x, modify_packet),
    store=False,
    filter="udp and dst port 5000"
)