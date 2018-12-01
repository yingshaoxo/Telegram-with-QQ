Server_ip = "182.294.242.181"
Token = '121899714:AAEXTAOSsuyFIb6Nydku3GhBM9sJtvstn8M'
The_group_id_you_wanna_forward = 0 # change it

if The_group_id_you_wanna_forward == 0:
    print(f"""
You have to set the The_group_id_you_wanna_forward varable to use this program.
    """)
    exit()


from king_chat import Client

client = Client(name="telegram", ip=Server_ip, port=5920)


from telegram.ext import Updater
from telegram import Bot

updater = Updater(token=Token)
dispatcher = updater.dispatcher
last_user_id = None


def format_msg(user_name, text):
    text = text.strip(' \n')
    return '{user_name}:\n\n\n{text}'.format(user_name=user_name, text=text)

def echo(bot, update):
    global The_group_id_you_wanna_forward
    global last_user_id
    user_name = update.message.from_user.full_name

    print('Your goup id: ', update.message.chat_id)
    if The_group_id_you_wanna_forward != 0:
        if update.message.chat_id == The_group_id_you_wanna_forward:
            client.send(format_msg(user_name, update.message.text))
    else:
        last_user_id = update.message.chat_id
        client.send(format_msg(user_name, update.message.text))

from telegram.ext import MessageHandler, Filters
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


@client.on_received
def on_received(protocol, text):
    global Token, Bot
    my_bot = Bot(token=Token)

    global The_group_id_you_wanna_forward
    global last_user_id

    print(text)
    if The_group_id_you_wanna_forward != 0:
        my_bot.send_message(chat_id=The_group_id_you_wanna_forward, text=text)
    elif last_user_id != None:
        my_bot.send_message(chat_id=last_user_id, text=text)


client.start(wait=False)
updater.start_polling()
