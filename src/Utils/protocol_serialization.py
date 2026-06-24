import json
from collections.abc import Callable    
from scapy.packet import Packet, Raw, bind_layers
from scapy.layers.inet import IP, UDP
from scapy.fields import Field, EnumField, ShortField, XByteField, IntEnumField
from Attacks.FieldModification import modify_field

class ProtocolEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Packet):
            return {
                'name': obj.name,
                'fields_desc': [{'name': field.name, 'default': field.default, 'fmt': field.fmt}
                                for field in obj.fields_desc if not isinstance(field, EnumField)],
                'enum_fields_desc': [{'name': field.name, 'default': field.default, 'enum': field.i2s, 'fmt': field.fmt}
                                     for field in obj.fields_desc if isinstance(field, EnumField)]
            }
        return super().default(obj)

def as_protocol(dct):
    if 'name' in dct and 'fields_desc' in dct:
        fields_desc = []
        for field in dct['fields_desc']:
            fields_desc.append(Field(field['name'], field['default'], field['fmt']))
        for field in dct['enum_fields_desc']:
            if 'I' in field['fmt']:
                enum_dict = {int(k): v for k, v in field['enum'].items()}
            else:
                enum_dict = {k: v for k, v in field['enum'].items()}
            fields_desc.append(EnumField(field['name'], field['default'], enum_dict, field['fmt']))
        return type(dct['name'], (Packet,), {"name": dct['name'], "fields_desc": fields_desc})
    return dct
    
if __name__ == "__main__":
    class Disney(Packet):
        name = "DisneyPacket"
        # fields_desc=[ ShortField("mickey",5),
        #              XByteField("minnie",3) ,
        #              IntEnumField("donald" , 1 ,
        #                   { 1: "happy", 2: "cool" , 3: "angry" } ) ]
        fields_desc = [
            Field("mickey", 5, "H"),
            Field("minnie", 3, "B"),
            EnumField("donald", 1, {1: "happy", 2: "cool", 3: "angry"}, fmt="I")
        ]
    disney_json = json.dumps(Disney(), cls=ProtocolEncoder)
    print(disney_json)
    disney_obj = json.loads(disney_json, object_hook=as_protocol)
    print(disney_obj)
    print(disney_obj.donald.i2s)

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