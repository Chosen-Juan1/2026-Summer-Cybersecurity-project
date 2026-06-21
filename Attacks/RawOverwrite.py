from scapy.all import Raw, send, IP, UDP
def overwrite_raw_contents(packet):
    #this one just swaps the raw contents of a packet if they have one
    print("=== Packet intercepted, modifying and resending ===")
    packet[Raw].load = b"I don't like either >:)"
    # dest = packet[IP].dst
    # souPort = packet[UDP].sport
    # desPort = packet[UDP].dport
    rawMsg = b"I don't like either >:)"
    newPacket = IP(dst=packet[IP].dst) / UDP(sport=packet[UDP].sport, dport=packet[UDP].dport) / Raw(load=rawMsg)
    newPacket.show2()
    send(newPacket)