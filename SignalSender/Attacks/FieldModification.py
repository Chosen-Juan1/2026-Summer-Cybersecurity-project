from scapy.packet import Packet
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw

def ModifyField(layer: Packet, field_name: str, new_value):
    setattr(layer, field_name, new_value)
    return layer


if __name__ == "__main__":
    packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))
    print(packet.show2())
    packet = ModifyField(packet, "sport", 4001)
    print(packet.show2())