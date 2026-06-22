from scapy.all import Raw, AsyncSniffer, send, IP, UDP, sniff
import subprocess
from RawOverwrite import overwrite_raw_contents
from Flooding import flood_destination
#^^^note about this, apperantly docker files don't copy folders into containers, they dump it all into a local directory :|
import time
# import random
from scapy.config import conf
conf.debug_dissector = 2 #<- apperantly, this is used for longer debug msgs
time.sleep(3) #<- need to give receiver some time to boot up

def listen_to_packets(packet):
    #i want this one to be the default man in the middle behaviour, listening mode
    print("=== Packet Snooped ===", flush=True)
    packet.show2()
    #modify the packet's RAW contents 



sniff( iface="eth0",
           prn=flood_destination,
             store=False,
            filter="udp and port 5000", #this if we only want to attack the receiver,
            #  filter="udp and (port 5000 or port 4000)",
             count = 1)



#Confirmed working:
# *Listen_to_packets (base behaviour)
# *RawOverwrite (wait for a bit and check the sender/receiver logs)
# *Flooding


# sniffer = AsyncSniffer(
#             iface="eth0",
#             prn=listen_to_packets,
#             store=False,
#             filter="udp and (port 5000 or port 4000)",
#             count=1
#         )

#.

# while True:
#     try:
#         # primero se verifica que el container que se desea este activo, sino, no se hace nah.
#         s = subprocess.check_output('docker ps | grep receiver', shell=True) #<- esto tira error si receiver no esta prendido
#         print(s)
#         sniffer.start()

#     except: 
#         if(sniffer.running):
#             sniffer.stop()
#         print("Container Dead")
#         break

    # # if KeyboardInterrupt:
    # #     print("Stopping sniffer...", flush=True)
    # #     sniffer.stop()

    # try:
    #     while True:
    #         print("Still sniffing...", flush=True)
    #         sleep(5)
    # except KeyboardInterrupt:
    #         print("Stopping sniffer...", flush=True)
    #         sniffer.stop()



