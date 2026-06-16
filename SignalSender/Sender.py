from scapy.all import IP, UDP, Raw, send, sr1
from Attacks.Fuzzing import Fuzzing
import time

# for x in range(0, 10):
#     #imma attmept to send the packet 10 times every 5 seconds
#     send(IP(dst="receiver") / UDP(dport=5000) / Raw(load="Hello receiver"))

# send(IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Hello receiver"))
time.sleep(5)

packet = (IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

# packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

sr1(packet)
print("Packet sent")
packet[Raw].load = b"Bad morning, receiver >:)"
badPacket = packet

#Fuzzing test:

badPacket = Fuzzing(badPacket)
print("Modified packet sent")

# sr1(badPacket)



# if __name__ == "__main__":
#     packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

#     payload = Fuzzing(packet)
#     print(payload.show2())


