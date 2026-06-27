from time import sleep
from dotenv import load_dotenv
from os import getenv
from scapy.all import sniff, IP, UDP, Raw, AsyncSniffer, sr1
from Server.databaseTest import dbTest

def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    packet.show2()
    sleep(5)
    print("=== Preparing response ===")
    query = packet[Raw].load
    print(query)
    res = str(dbTest(query))
    res = bytes(res,encoding='utf-8')
    print("=== Sending Response ===")
    packet = (IP(dst="client") / UDP(sport=5000, dport=packet[UDP].sport) / Raw(load=res))
    sr1(packet)

    # if(Raw in packet):
    #     print(f"Information sent with flush: {packet[Raw].load}\n", flush=True)


sniffer = AsyncSniffer(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp dst port 5000",
    count=50
)

sniffer.start()

try:
    while True:
        print("Still sniffing...", flush=True)
        sleep(5)
except KeyboardInterrupt:
    print("Stopping sniffer...", flush=True)
    sniffer.stop()
