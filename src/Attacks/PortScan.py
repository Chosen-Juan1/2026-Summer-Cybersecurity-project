from scapy.all import Raw, send, IP, UDP, sr1
from time import sleep

def portScan(packet):
    packet.show2()
    destContainer = packet[IP].dst
    destPort = packet[UDP].dport
    print(f"\n packet dest {destContainer} and port dest {destPort}")


    #ima see if there are ports after the captured packet's dport
    
#ima first try with 20 above and 20 below
    listOfOpenPorts = []
    listOfOpenPorts.append(destPort)
    for ports in range(1,21):
        inspecting = destPort + ports
        # send((IP(dst=packet[IP].dst) / UDP(sport=packet[UDP].sport, dport=packet[UDP].sport) / Raw(load=rawMsg)))
        packet = (IP(dst=destContainer) / UDP(sport=4001, dport=inspecting) / Raw(load="Knock-knock"))
        answer = sr1(packet)
        sleep(1) #<- enable if too fast
        if(answer != None):
            listOfOpenPorts.append(inspecting)
    print("=== Ascending ports scanned, now on to the lower ones ===", flush=True)

    for ports in range(1,21):
        inspecting = destPort - ports
        if(inspecting > 0):
            packet = (IP(dst=destContainer) / UDP(sport=4001, dport=inspecting) / Raw(load="Knock-knock"))
            answer = sr1(packet)
            sleep(1)
            if(answer != None):
                listOfOpenPorts.append(inspecting)
    print("=== Descending ports scanned, now on to the final preperations ===", flush=True)

    return listOfOpenPorts
