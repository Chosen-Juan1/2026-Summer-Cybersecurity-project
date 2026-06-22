from scapy.all import IP, UDP, Raw, send, sr1, sniff, AsyncSniffer
from time import sleep
def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    packet.show2()
    sleep(7)
    print("=== Sending Response ===")
    sr1(IP(dst="receiver") / UDP(sport=4000, dport=packet[UDP].sport) / Raw(load=b"Yuh uh"))

# for x in range(0, 10):
#     #imma attmept to send the packet 10 times every 5 seconds
#     send(IP(dst="receiver") / UDP(dport=5000) / Raw(load="Hello receiver"))

# send(IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Hello receiver"))
packet = (IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Waffles are better than pancakes!!!"))

    # packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

ans = sr1(packet)
sniffer = AsyncSniffer(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp dst port 4000",
    count=50
) #Im setting up count limits cause leaving these fellas running causes docker to break, requiring a computer reset.

sniffer.start()

try:
    while True:
        print("Still sniffing...", flush=True)
        sleep(4)
except KeyboardInterrupt:
    print("Stopping sniffer...", flush=True)
    sniffer.stop()
#<- apperantly this needs a specific linux lib, added it to the docker file

# print("Packet sent")
# packet[Raw].load = b"Bad morning from mac, receiver >:)"
# badPacket = packet

#Fuzzing test:

# badPacket = Fuzzing(badPacket)
# print("Modified packet sent")

# sr1(badPacket)

    # if(Raw in packet):
    #     print(f"Information sent with flush: {packet[Raw].load}\n", flush=True)







# if __name__ == "__main__":
#     packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

#     payload = Fuzzing(packet)
#     print(payload.show2())


