# server
from king_chat import Server

server = Server(ip="0.0.0.0", port=5920)

@server.on_received
def handle(protocol, text):
    print(protocol.name, ": ", text)
    protocol.send_to_all_except_sender(text)

server.start(wait=True)
