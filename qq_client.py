Server_ip = "182.294.242.181"
Docker_CQhttp_address = 'http://127.0.0.1:5700/'
The_QQ_group_number_you_wanna_forward = 0

if The_QQ_group_number_you_wanna_forward == 0:
    print(f"""
You have to set the The_QQ_group_number_you_wanna_forward varable to use this program.
    """)
    exit()


from king_chat import Client

client = Client(name="qq", ip='127.0.0.1', port=5920)


from cqhttp import CQHttp
from datetime import datetime

bot = CQHttp(api_root=Docker_CQhttp_address)
last_context = None


def in_blacklist(name):
    blacklist = [
        "腾讯新闻",
    ]
    if name in blacklist:
        return True
    else:
        return False


def filter(text):
    """
    作业 or 交
    页 and 题
    报名 or 缴费
    课 and 上
    面试 or 校招
    """
    if ('新闻' in text):
        return ''

    if ('作业' in text) or ('交' in text):
        return text
    elif ('页' in text) and ('题' in text):
        return text
    elif ('报名' in text) or ('缴费' in text):
        return text
    elif ('课' in text) and ('上' in text):
        return text
    elif ('面试' in text) or ('校招' in text):
        return text

    return ''


def format_msg(user_name, text):
    text = text.strip(' \n')
    return '{user_name}:\n\n\n{text}'.format(user_name=user_name, text=text)


last_time = datetime.now()
def call_me():
    global last_time
    now = datetime.now()
    last_time = now


def how_much_seconds_has_passed_since_last_time_you_call_me():
    global last_time
    now = datetime.now()
    result = (now - last_time).seconds
    return result


@bot.on_message()
def handle_msg(context):
    global The_QQ_group_number_you_wanna_forward
    global last_context
    global bot

    user_id = context['user_id']
    user_info = bot.get_stranger_info(user_id=user_id)
    user_name = user_info['nickname']
    text = context['message']

    """
    if The_QQ_group_number_you_wanna_forward != 0:
        client.send(format_msg(user_name, text))
    else:
        last_context = context
        client.send(format_msg(user_name, text))
    """

    if in_blacklist(user_name):
        return

    if context['message_type'] == 'group':
        group_id = context['group_id']
        if group_id != The_QQ_group_number_you_wanna_forward:
            new_text = filter(context['message'])
            if new_text != "":
                client.send(format_msg(user_name, new_text))

                call_me()
                last_context = context
        else:
            client.send(format_msg(user_name, text))
    else:
        client.send(format_msg(user_name, text))
        call_me()
        last_context = context

    #bot.send(context, '你好呀，下面一条是你刚刚发的：')
    # return {'reply': context['message'], 'at_sender': False}


@client.on_received
def on_received(protocol, text):
    global The_QQ_group_number_you_wanna_forward
    global last_context
    global bot

    print(text)
    seconds_since_last_time_other_group_have_sent_msg = how_much_seconds_has_passed_since_last_time_you_call_me()
    minutes = seconds_since_last_time_other_group_have_sent_msg / 60
    if minutes >= 60 * 3:
        bot.send_group_msg(
            group_id=The_QQ_group_number_you_wanna_forward, message=text)
    elif last_context != None:
        bot.send(last_context, text)
    else:
        bot.send_group_msg(
            group_id=The_QQ_group_number_you_wanna_forward, message=text)


client.start(wait=False)
bot.run(host='0.0.0.0', port=8080)
