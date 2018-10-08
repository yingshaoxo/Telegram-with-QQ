Server_ip = "182.294.242.181"
Docker_CQhttp_address = 'http://127.0.0.1:5700/'
The_QQ_group_number_you_wanna_forward = 0


from king_chat import Client

client = Client(name="qq", ip=Server_ip, port=5920)


from cqhttp import CQHttp

bot = CQHttp(api_root=Docker_CQhttp_address)
last_context = None

@bot.on_message()
def handle_msg(context):
    if The_QQ_group_number_you_wanna_forward != 0:
        client.send(context['message'])
    else:
        global last_context
        last_context = context
        client.send(context['message'])
    #bot.send(context, '你好呀，下面一条是你刚刚发的：')
    #return {'reply': context['message'], 'at_sender': False}


@client.on_received
def on_received(protocol, text):
    global last_context
    global bot

    print(text)
    if The_QQ_group_number_you_wanna_forward != 0:
        bot.send_group_msg(group_id=The_QQ_group_number_you_wanna_forward, message=text)
    elif last_context != None:
        bot.send(last_context, text)


client.start(wait=False)
bot.run(host='0.0.0.0', port=8080)
