import os
import signal
import sys


from scapy.all import IP, UDP, Raw, AsyncSniffer
from time import sleep

def handle_packet(packet):
    print("=== Packet Snooped ===", flush=True)
    packet.show2()
    # if(Raw in packet):
    #     print(f"Information sent with flush: {packet[Raw].load}\n", flush=True)




sniffer = AsyncSniffer(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp and (port 5000 or port 4000)"
)

sniffer.start()

# if KeyboardInterrupt:
#     print("Stopping sniffer...", flush=True)
#     sniffer.stop()

try:
    while True:
        print("Still sniffing...", flush=True)
        sleep(5)
except KeyboardInterrupt:
        print("Stopping sniffer...", flush=True)
        sniffer.stop()


