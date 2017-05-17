import telebot
import asyncore
import threading

TOKEN = "add your telegram bot TOKEN"
CHAT_ID = -1001120909649
bot = telebot.AsyncTeleBot(TOKEN)

SERVER_ADDR = '127.0.0.1'

class MySocketClient(asyncore.dispatcher):
    
    def __init__(self, server_address):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect(server_address)

    def handle_read(self):
        data = self.recv(8192)
        if data:
            try:
                bot.send_message(CHAT_ID, data.decode('gb2312', 'ignore')).wait()
            except:
                bot.send_message(CHAT_ID, data.decode('utf-8', 'ignore')).wait()
            else:
                pass
            #print(data)

client = MySocketClient((SERVER_ADDR, 5920))


def msg_format(name, text):
    if text.count('\n') >= 1:
        text = '[{}]: \n{}'.format(name, text)
    else:
        text = '[{}]: {}'.format(name, text)
    return text

@bot.message_handler(commands=['chat_id'])
def handle(msg):
    if msg.chat.type == 'supergroup':
        bot.reply_to(msg.chat.id, 'Chat_id of this group:\n\n{}'.format(str(msg.chat.id)))
        
@bot.message_handler(content_types=['text'])
def handle(msg):
    if msg.chat.type == 'supergroup' and msg.chat.id == CHAT_ID:
        real_msg = msg.text
        try:
            real_msg = msg_format(msg.from_user.username, real_msg)
            print(real_msg)
            real_msg = real_msg.encode('gb2312', 'ignore')
            client.send(real_msg)
        except:
            pass
            
socket_thread = threading.Thread(target=asyncore.loop)
socket_thread.start()

bot_thread = threading.Thread(target=bot.polling)
bot_thread.start()
