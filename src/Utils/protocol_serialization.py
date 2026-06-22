from scapy.base_classes import Packet_metaclass, Field_metaclass
from scapy.fields import Field, EnumField, ShortField, XByteField, IntEnumField
from scapy.packet import Packet
from scapy.layers.inet import IP, UDP
from scapy.packet import Raw
import json
    
class ProtocolEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Packet):
            return {
                'name': obj.name,
                'fields_desc': [{'name': field.name, 'default': field.default, 'fmt': field.fmt} for field in obj.fields_desc if not isinstance(field, EnumField)],
                'enum_fields_desc': [{'name': field.name, 'default': field.default, 'enum': field.i2s, 'fmt': field.fmt} for field in obj.fields_desc if isinstance(field, EnumField)]
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