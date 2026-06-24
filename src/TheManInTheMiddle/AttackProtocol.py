import json
from collections.abc import Callable    
from scapy.packet import Packet, Raw, bind_layers
from scapy.layers.inet import IP, UDP
from scapy.fields import Field, EnumField, ShortField, XByteField, IntEnumField
from Utils.protocol_serialization import ProtocolEncoder, as_protocol
from Attacks.FieldModification import modify_field

LAYER_MAP = {
    "IP": IP,
    "UDP": UDP,
}

def bind_protocol(protocol: list[tuple[str, bool]], layer_jsons: dict[str, str]):
    """
    Binds a list of layers together. Builds custom layers.
    """
    protocol_layers = []
    for layer_name, is_custom in protocol:
        if is_custom:
            layer_json = layer_jsons[layer_name]
            layer_obj = json.loads(layer_json, object_hook=as_protocol)
        elif layer_name in LAYER_MAP:
            # If it's not a custom layer, we assume it's a standard Scapy layer
            layer_obj = LAYER_MAP.get(layer_name)
        else:
            raise ValueError(f"Layer {layer_name} is not recognized as a standard Scapy layer or a custom layer.")
        protocol_layers.append(layer_obj)

    # Only bind custom layers
    indices = [i for i, (_, is_custom) in enumerate(protocol) if i > 0 and (is_custom or protocol[i - 1][1])]
    for i in indices:
        bind_layers(protocol_layers[i - 1], protocol_layers[i])

def demo():
    # Example usage
    protocol = [("IP", False), ("UDP", False), ("DisneyPacket", True)]
    layer_jsons = {
        "DisneyPacket": json.dumps({
            'name': 'DisneyPacket',
            'fields_desc': [
                {'name': 'mickey', 'default': 5, 'fmt': 'H'},
                {'name': 'minnie', 'default': 3, 'fmt': 'B'}
            ],
            'enum_fields_desc': [
                {'name': 'donald', 'default': 1, 'enum': {1: "happy", 2: "cool", 3: "angry"}, 'fmt': 'I'}
            ]
        })
    }
    bind_protocol(protocol, layer_jsons)
    
    from scapy.sendrecv import AsyncSniffer, send
    disney_layer = json.loads(layer_jsons["DisneyPacket"], object_hook=as_protocol)
    def sniffer_callback(packet: Packet):
        print("Received:", packet.summary())
        print(packet["DisneyPacket"].mickey)
        modified_packet = modify_field(packet, "DisneyPacket", "mickey", 99)
        print(modified_packet["DisneyPacket"].mickey)

    sniffer = AsyncSniffer(
        filter="udp port 5000",
        store=False,
        prn=sniffer_callback
    )
    sniffer.start()
    send(IP(dst="10.0.0.2")/UDP(dport=5000)/disney_layer(mickey=10, minnie=20, donald=2))
    # send(IP(dst="10.0.0.2")/UDP(dport=5000))
    sniffer.stop()