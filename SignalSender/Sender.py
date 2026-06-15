from scapy.all import IP, UDP, Raw, send, sr1
import time

# for x in range(0, 10):
#     #imma attmept to send the packet 10 times every 5 seconds
#     time.sleep(5)
#     send(IP(dst="receiver") / UDP(dport=5000) / Raw(load="Hello receiver"))

# send(IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Hello receiver"))
packet = (IP(dst="receiver") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))
sr1(packet)
print("Packet sent")
packet[Raw].load = b"Bad morning, receiver >:)"
badPacket = packet
print("Modified packet sent")

sr1(badPacket)


####matlab simulink

##create the account @upr.edu, then swittch to @uprm

##RTlab 2022 ver

#using udp


#for power system comms
#madbus (orgs the info so that its eaiser to read)

#IEC 61-50

#Goose communications
###^^^^ they have cyber blocks but the liscense is expensive

#dmp3


#mains source of cyber threats, change what the system belives its current status


##Exata cps (core simulator

#cortellmenL a lot of sun but no bats to put it)


#learn the commands sent

#4-5 cyber scenarios

##an attacker 

# https://attack.mitre.org/

#cve attack

#fuzzing