import sys
sys.path.append(".")
import datetime as dt
import streamlit as st
import time
from scapy.packet import Packet, Raw
from TheManInTheMiddle.TuesdayDemo_man import Interceptor, Attack, Source

st.session_state.last_timestamp = st.session_state.get("last_timestamp", dt.datetime.min)

@st.cache_resource
def load_interceptor():
    interceptor = Interceptor()
    interceptor.sniffer.start()
    return interceptor

interceptor = load_interceptor()

st.header("The Man")

attack = st.selectbox(
    "Select an attack",
    ["None", "Overwrite", "Flood"]
)

interceptor.attack_type = {
    "None": None,
    "Overwrite": Attack.OVERWRITE,
    "Flood": Attack.FLOOD
}[attack]

def get_text_from_packet(packet: Packet) -> str:
    if Raw in packet:
        return packet[Raw].load.decode(errors='ignore')
    return "No data found in packet."

if interceptor.intercepted_packets:
    st.subheader("Intercepted Packets")
    for i, intercepted_packet in tuple(enumerate(interceptor.intercepted_packets))[::-1]:
        with st.container(border=True):
            st.write(f"Packet {i + 1}:")
            source = {
                Source.CLIENT: "Client",
                Source.SERVER: "Server"
            }[intercepted_packet.source]
            source_col, timestamp_col = st.columns(2)
            with source_col:
                st.write(f"Source: {source}")
            with timestamp_col:
                st.write(f"Timestamp: {intercepted_packet.timestamp}")
            
            if intercepted_packet.source == Source.CLIENT:
                received_text = get_text_from_packet(intercepted_packet.received_packet)
                if intercepted_packet.modified_packet:
                    modified_text = get_text_from_packet(intercepted_packet.modified_packet)
                    received_col, modified_col = st.columns(2)
                    with received_col:
                        st.write("Received Packet:")
                        st.text(received_text)
                    with modified_col:
                        st.write("Modified Packet:")
                        st.text(modified_text)
                else:
                    st.write("Received Packet:")
                    st.text(received_text)
            else:
                st.write("TODO")

while True:
    if interceptor.intercepted_packets and interceptor.intercepted_packets[-1].timestamp > st.session_state.last_timestamp:
        st.session_state.last_timestamp = interceptor.intercepted_packets[-1].timestamp
        st.rerun()
    else:
        time.sleep(1)