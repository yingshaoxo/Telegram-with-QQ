import asyncio
import threading

import time
from datetime import datetime


BotQQ = '296209157' # QQ number
GroupID = '208408255' # Group number

SERVER_ADDR = '127.0.0.1' # VPS address


class ClientProtocol(asyncio.Protocol):
    def __init__(self, control, loop):
        self.loop = loop
        self.control = control

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            text = data.decode('utf-8', 'ignore')
        except:
            return

        if text == '*1*':
            self.control.last_connection_time = datetime.now()
            return 
        
        print(text)
        mybot.SendTo(goal_group, text)

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.transport.close()


class ConnectionControl():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.is_stop = False
        
        print('connect')
        if self.reconnect():
            threading.Thread(target=self.receive_msg).start()
            threading.Thread(target=self.detect_if_offline).start()
        else:
            exit()


    def reconnect(self):
        try:
            self.coro = self.loop.create_connection(lambda: ClientProtocol(self, self.loop),
                                          SERVER_ADDR, 5920)
            self.transport, self.protocol = self.loop.run_until_complete(self.coro)
            
            self.last_connection_time = datetime.now()
        except Exception as e:
            print(e)
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
        if self.transport != None:
            if self.transport.is_closing():
                self.reconnect()
            self.transport.write(msg.encode("utf-8"))



from qqbot import QQBotSlot as qqbs, RunBot

@qqbs
def onStartupComplete(bot):
    global groupList, buddyList, discList, goal_group
    bot.Update('group')
    groupList = bot.List('group')
    bot.Update('buddy')
    buddyList = bot.List('buddy')
    bot.Update('discuss')
    discList = bot.List('discuss')
    
    goal_group = searchByQQ(GroupID, 'group')
    if goal_group is None:
        print("Group number error!")
        exit() 

    global conn, mybot
    conn = ConnectionControl()
    mybot = bot

@qqbs
def onQQMessage(bot, contact, member, content):
    if not contact.ctype == 'group': # Only receive group message
        return

    if contact.name == goal_group.name:
        conn.send_msg(msg_format(member.name, content))
        #bot.SendTo(ct, "Check!")
    elif content == 'STOP':
        bot.SendTo(contact, "I have stopped")
        bot.Stop()

def searchByQQ(qqID, cinfo):
    if cinfo == 'group':
        contacts = groupList
    elif cinfo == 'buddy':
        contacts = buddyList
    elif cinfo == 'discuss':
        contacts = discList
    else:
        return
    for contact in contacts:
        if contact.qq == qqID:
            return contact

def msg_format(name, text):
    if text.count('\n') >= 1:
        text = '[{}]: \n{}'.format(name, text)
    else:
        text = '[{}]: {}'.format(name, text)
    return text


try:
    RunBot()

except KeyboardInterrupt:
    conn.is_stop = True
