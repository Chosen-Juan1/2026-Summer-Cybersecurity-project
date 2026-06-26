from scapy.sendrecv import send
from scapy.packet import Packet, Raw
from scapy.layers.inet import IP, UDP
from dotenv import load_dotenv
from os import getenv
load_dotenv()
DEBUG = getenv("DEBUG", "0").lower() == "1"

def apply(packet: Packet, modifier, recalc=True, drop_datalink_layer=True) -> Packet:
    """
    Applies a modification function to a packet and returns the modified packet.

    :param packet: The original packet to be modified.
    :param modifier: A function that takes a packet as input and returns a modified packet.
    :return: The modified packet.
    """
    if DEBUG:
        print("=== Original Packet ===", flush=True)
        packet.show2()
    modified_packet: Packet = modifier(packet)
    if drop_datalink_layer and modified_packet.haslayer(IP):
        modified_packet = modified_packet[IP]  # Drop datalink layer if present
    if recalc:
            # Remove existing to force recalculation
            del modified_packet[IP].len
            del modified_packet[IP].chksum
            if UDP in modified_packet:
                del modified_packet[UDP].len
                del modified_packet[UDP].chksum
    if DEBUG:
        print("=== Modified Packet ===", flush=True)
        modified_packet.show2()
    return modified_packet

def apply_and_send(packet: Packet, modifier, recalc=True, drop_datalink_layer=True):
    """
    Applies a modification function to a packet and sends it.

    :param packet: The original packet to be modified.
    :param modifier: A function that takes a packet as input and returns a modified packet.
    """
    send(apply(packet, modifier, recalc=recalc, drop_datalink_layer=drop_datalink_layer))