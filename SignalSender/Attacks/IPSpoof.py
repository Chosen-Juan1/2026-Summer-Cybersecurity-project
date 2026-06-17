from scapy.layers.inet import IP, UDP
from scapy.packet import Raw


def IPSpoof(packet, spoofed_ip="192.168.1.100"):
    packet[IP].src = spoofed_ip
    return packet


if __name__ == "__main__":
    packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))
    print(packet.show2())
    packet = IPSpoof(packet)
    print(packet.show2())