from scapy.packet import Packet
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw

def get_layers(packet: Packet):
    layers = []
    current_layer = packet
    while current_layer:
        layers.append(current_layer.name)
        current_layer = current_layer.payload
    return layers

def get_fields(packet: Packet, layer_name: str):
    layer = packet.getlayer(layer_name)
    if layer:
        return layer.fields
    else:
        raise ValueError(f"Layer {layer_name} not found in the packet.")

def ModifyField(packet: Packet, layer_name: str, field_name: str, new_value):
    layer = packet.getlayer(layer_name)
    setattr(layer, field_name, new_value)
    return packet

if __name__ == "__main__":
    packet = (IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=b"Good morning, receiver :)"))
    print(get_layers(packet))
    print(get_fields(packet, "UDP"))
    ModifyField(packet, "UDP", "sport", 4001)
    print(packet[UDP].sport)