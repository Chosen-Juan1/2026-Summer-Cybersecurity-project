from scapy.layers.inet import IP, UDP
from scapy.packet import Packet, Raw


DEFAULT_INJECTION = b"[SIMULATED]"
DEMO_PAYLOAD = b"Hello, receiver this is some data."
DEMO_INSERTION = b"<INJECTED>"


def describe_packet(packet: Packet) -> str:
	"""Return a compact payload summary for demo output."""
	if Raw in packet:
		return repr(bytes(packet[Raw].load))
	return "<no raw payload>"


def simulate_byte_injection(packet: Packet, injection: bytes = DEFAULT_INJECTION, offset: int | None = None):
	"""Insert bytes into the Raw payload to simulate packet tampering locally."""
	print("=== Simulated byte-injection demo ===", flush=True)

	if Raw not in packet:
		# If there is no payload yet, attach the simulated bytes as a new Raw layer.
		return packet / Raw(load=injection)

	original_payload = bytes(packet[Raw].load)
	# Default to the middle of the payload so the insertion is obvious in the demo.
	insert_at = len(original_payload) // 2 if offset is None else offset
	insert_at = max(0, min(insert_at, len(original_payload)))

	# Work on a copy so the original packet remains unchanged for comparison.
	mutated_packet = packet.copy()
	mutated_packet[Raw].load = original_payload[:insert_at] + injection + original_payload[insert_at:]
	return mutated_packet


def build_demo_packet() -> Packet:
	"""Create a small UDP packet that is easy to inspect in a demo."""
	# This keeps the example simple and local to 127.0.0.1.
	return IP(dst="127.0.0.1") / UDP(sport=4000, dport=5000) / Raw(load=DEMO_PAYLOAD)


if __name__ == "__main__":
	packet = build_demo_packet()
	print("Before:")
	print(f"  payload: {describe_packet(packet)}")
	print(packet.show2())
	# Insert the demo marker so the before/after difference is easy to see.
	packet = simulate_byte_injection(packet, injection=DEMO_INSERTION)
	print("After:")
	print(f"  payload: {describe_packet(packet)}")
	print(packet.show2())
