from scapy.all import IP, UDP, Raw, send, sr1
import time

# for x in range(0, 10):
#     #imma attmept to send the packet 10 times every 5 seconds
#     time.sleep(5)
#     send(IP(dst="receiver") / UDP(dport=5000) / Raw(load="Hello receiver"))

# send(IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Hello receiver"))
packet = (IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))
sr1(packet)
print("Packet sent")
packet[Raw].load = b"Bad morning, receiver >:)"
badPacket = packet
print("Modified packet sent")

sr1(badPacket)
