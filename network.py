from packing import *
from unpacking import *

def send_receive_message(server_ip: str, question: Message) -> Message:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message_to_bytes(question), (server_ip, 53))
    data_orig, _ = sock.recvfrom(1024)
    return message_from_bytes(data_orig)