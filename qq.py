import asyncio
import threading

import time
from datetime import datetime


BotQQ = '296209157' # QQ number
GroupID = '208408255' # Group number

SERVER_ADDRESS = '45.63.90.169' # VPS address


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

        if '*1*' in text:
            self.control.last_connection_time = datetime.now()
            return 
        
        #print(text)
        #print('You got', threading.active_count(), 'threadings.')
        mybot.SendTo(goal_group, text)

    def connection_lost(self, exc):
        print('The server closed the connection')
        #self.transport.close()


class ConnectionControl():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.is_stop = False
        
        try:
            self.coro = self.loop.create_connection(lambda: ClientProtocol(self, self.loop), SERVER_ADDRESS, 5920)
            self.last_connection_time = datetime.now()
            self.transport, self.protocol = self.loop.run_until_complete(self.coro)
        except:
            print("You need to make sure server is availablei.")
            exit()

        threading.Thread(target=self.receive_msg).start()
        threading.Thread(target=self.detect_if_offline).start()

    def reconnect(self):
        try:
            _, self.protocol = self.loop.run_until_complete(self.coro)
            self.transport.set_protocol(self.protocol)

            self.last_connection_time = datetime.now()
        except Exception as e:
            #print(e)
            print("No server available.")
            return False

        return True

    def detect_if_offline(self): #run every 3 seconds
        while True:
            if (datetime.now() - self.last_connection_time).total_seconds() > 45:
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
    global groupList_, buddyList_, discList_, goal_group
    bot.Update('group')
    groupList_ = bot.List('group')
    bot.Update('buddy')
    buddyList_ = bot.List('buddy')
    bot.Update('discuss')
    discList_ = bot.List('discuss')

    goal_group = searchByQQ(GroupID, 'group')
    if goal_group is None:
        print("Group number error!")
        exit() 
    #print('You got', threading.active_count(), 'threadings.')
    global conn, mybot
    conn = ConnectionControl()
    mybot = bot

@qqbs
def onQQMessage(bot, contact, member, content):
    if not contact.ctype == 'group': # Only receive group message
        return
    if member.qq == BotQQ: # Do not receive msgs from bot itself
        return

    if contact.name == goal_group.name:
        print('You got', threading.active_count(), 'threadings.')
        conn.send_msg(msg_format(member.name, content))
        #bot.SendTo(ct, "Check!")
    elif content == 'STOP':
        bot.SendTo(contact, "I have stopped")
        bot.Stop()

def searchByQQ(qqID, cinfo):
    if cinfo == 'group':
        contacts = groupList_
    elif cinfo == 'buddy':
        contacts = buddyList_
    elif cinfo == 'discuss':
        contacts = discList_
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
