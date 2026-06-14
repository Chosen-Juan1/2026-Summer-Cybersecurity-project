from scapy.all import IP, UDP, Raw, send
import time

# for x in range(0, 10):
#     #imma attmept to send the packet 10 times every 5 seconds
#     time.sleep(5)
#     send(IP(dst="receiver") / UDP(dport=5000) / Raw(load="Hello receiver"))

send(IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Hello receiver"))
print("Packet sent")
