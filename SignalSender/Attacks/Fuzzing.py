from scapy.all import IP, UDP, Raw, send, sr1, fuzz
#The goal is to fuzz many of the attributes 

def Fuzzing(packet):
    fuzzed = fuzz(packet)
    # listOfPackets = []

    # for ite in range(0,20):
    #     tempPak = packet
    #     if(ite % 5 == 0):
    #         tempPak[IP].load = fuzz(packet[IP])
    #     elif(ite %10 == 0):
    #         tempPak[UDP] = fuzz(packet[UDP])
    #     elif(ite % 15 == 0):
    #         #fuzz the source ip
    #         tempPak[Raw].load = fuzz(packet[Raw])
    #     else:
    #         tempPak[IP] = fuzz(packet[IP])
    #         tempPak[UDP] = fuzz(packet[UDP])
    #         tempPak[Raw].load = fuzz(packet[Raw])
    #     listOfPackets.append(tempPak)



    return fuzzed


if __name__ == "__main__":
    packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))

    payload = Fuzzing(packet)
    print(payload.show2())

