import time

from scapy.all import sniff, IP, UDP, Raw, AsyncSniffer, sr1
from time import sleep

def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    packet.show2()
    sleep(5)
    print("=== Sending Response ===")
    packet = (IP(dst="sender") / UDP(sport=5000, dport=packet[UDP].sport) / Raw(load=b"Nuh uh"))
    sr1(packet)

    # if(Raw in packet):
    #     print(f"Information sent with flush: {packet[Raw].load}\n", flush=True)


sniffer = AsyncSniffer(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp dst port 5000",
    count=10
)

sniffer.start()

try:
    while True:
        print("Still sniffing...", flush=True)
        sleep(5)
except KeyboardInterrupt:
    print("Stopping sniffer...", flush=True)
    sniffer.stop()


