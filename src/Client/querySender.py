from scapy.all import IP, UDP, Raw, send, sr1, sniff, AsyncSniffer
from time import sleep

def handle_packet(packet):
    print("=== Packet received ===", flush=True)
    response = packet[Raw].load
    print(response, flush=True)


packet = (IP(dst="postgres") / UDP(sport=4000, dport=5000) / Raw(load=b"select * from users;"))

sleep(2)

send(packet)

sniffer = AsyncSniffer(
    iface="eth0",
    prn=handle_packet,
    store=False,
    filter="udp dst port 4000",
    count=1
)

sniffer.start()

try:
    while True:
        print("Still sniffing...", flush=True)
        sleep(5)
except KeyboardInterrupt:
    print("Stopping sniffer...", flush=True)
    sniffer.stop()