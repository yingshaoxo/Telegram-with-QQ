import asyncio
import threading
import time

global connected_transport
connected_transport = dict()

class ServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        
        connected_transport.update({self.peername: transport})
        print('Connection from {}'.format(self.peername))

    def data_received(self, data):
        print('Data received:', data.decode('utf-8', 'ignore'))

        for i in [i for i in connected_transport.values() if i != self.transport]:
            i.write(data)

    def connection_lost(self, exc):
        print('Lost connection of {}'.format(self.peername))
        del connected_transport[self.peername]
        self.transport.close()


def are_you_ok():
    while True:
        for i in [i for i in connected_transport.values()]:
            i.write("*1*".encode('utf-8'))
        time.sleep(40)


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(ServerClientProtocol, '0.0.0.0', 5920)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    threading.Thread(target=are_you_ok).start()
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
