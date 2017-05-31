import asyncio
import threading

import time
from datetime import datetime


class ClientProtocol(asyncio.Protocol):
    def __init__(self, control, loop):
        self.loop = loop
        self.control = control

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        text = data.decode('utf-8', 'ignore')

        if text == "*1*":
            self.control.last_connection_time = datetime.now()
            return 

        print('Data received: {!r}'.format(text))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.transport.close()


class ConnectionControl():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.is_stop = False

        if self.reconnect():
            threading.Thread(target=self.receive_msg).start()
            threading.Thread(target=self.detect_if_offline).start()
        else:
            exit()


    def reconnect(self):
        try:
            self.coro = self.loop.create_connection(lambda: ClientProtocol(self, self.loop),
                                          '127.0.0.1', 5920)
            self.transport, self.protocol = self.loop.run_until_complete(self.coro)
            
            self.last_connection_time = datetime.now()
        except Exception as e:
            #print(e)
            print("No server available.")
            return False

        return True

    def detect_if_offline(self): #run every 3 seconds
        while True:
            if (datetime.now() - self.last_connection_time).total_seconds() > 45:
                self.transport.close()
                self.reconnect()
                print("I just reconnected the server.")
            time.sleep(3)
            if self.is_stop == True:
                return

    def receive_msg(self):
        while True:
            self.loop.run_until_complete(self.coro)
            time.sleep(1)
            if self.is_stop == True:
                return

    def send_msg(self, msg):
        if conn.transport != None:
            if conn.transport.is_closing():
                self.reconnect()
            self.transport.write(msg.encode("utf-8"))
try:
    conn = ConnectionControl()

    while True:
        conn.send_msg(input("say something: "))

except KeyboardInterrupt:
    conn.is_stop = True
