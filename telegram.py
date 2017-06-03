import telebot
import asyncio
import threading

from datetime import datetime
import time

TOKEN = "121899714:AAF3xShKMc52iV5yN93fiIjOH98ZXP1zcOc"#"add your telegram bot TOKEN"
bot = telebot.AsyncTeleBot(TOKEN)

master_id = 131513300

global share_var
share_var = {'chat_id': -1001120909649}

SERVER_ADDR = '127.0.0.1'


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
        bot.send_message(share_var['chat_id'], text).wait()

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
                                          SERVER_ADDR, 5920)
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
        if self.transport != None:
            if self.transport.is_closing():
                self.reconnect()
            self.transport.write(msg.encode("utf-8"))


def msg_format(name, text):
    if text.count('\n') >= 1:
        text = '[{}]: \n{}'.format(name, text)
    else:
        text = '[{}]: {}'.format(name, text)
    return text

@bot.message_handler(commands=['chat_id'])
def handle(msg):
    if msg.chat.type == 'supergroup':
        reply = 'Chat_id of this group:\n\n{}'.format(str(msg.chat.id))
        reply += '\n\n' + '-'*20 + '\n\n' + 'Who sent this message:\n\n{}'.format(str(msg.from_user.id))
        bot.reply_to(msg, reply)
        
@bot.message_handler(content_types=['text'])
def handle(msg):
    if msg.from_user.id == master_id:
        share_var.update({'chat_id': msg.chat.id})
    if msg.chat.type == 'supergroup' and msg.chat.id == share_var['chat_id']:
        real_msg = msg.text
        try:
            real_msg = msg_format(msg.from_user.username, real_msg)
            print(real_msg)
            conn.send_msg(real_msg)
        except:
            pass
            
try:
    conn = ConnectionControl()

    bot.polling()

except KeyboardInterrupt:
    conn.is_stop = True
