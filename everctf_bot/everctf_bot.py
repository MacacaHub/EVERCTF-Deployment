from everctf_bot_data import token
from telegram import *
from telegram.ext import *
import re
import os

bot = Bot(token)
IPv4_re = '(\d{1,3}\.){3}[0-9]{1,3}(:\d+)?'
ip_dict = {}
phase = 'none'

def get_ip_list(chat_id):
    global ip_dict
    check_and_add_chat_id(chat_id)
    return ip_dict[chat_id]

def check_and_add_chat_id(chat_id):
    global ip_dict
    if not chat_id in ip_dict.keys():
        ip_dict[chat_id] = []
        update_chat_id_list(chat_id)

def add_phase(update, context):
    global phase
    phase = 'add'
    update.message.reply_text('input the ip you want to monitor\nN to exit')

def rm_phase(update, context):
    global phase
    phase = 'rm'
    update.message.reply_text('input the ip you want to remove\nN to exit')

def show_phase(update, context):
    global phase
    phase = 'show'
    chat_id = update.effective_chat.id
    ip_list = get_ip_list(chat_id)
    if len(ip_list) == 0:
        msg = 'you have not set any ip'
    else:
        msg = '\n'.join(ip_list)
    send_message_to(chat_id, msg)

def save_phase(update, context):
    global phase
    phase = 'save'
    chat_id = update.effective_chat.id
    ip_list = get_ip_list(chat_id)
    f = open(str(chat_id), 'w')
    for ip in ip_list:
        f.write(ip+'\n')
    f.close()
    send_message_to(chat_id, f'ip list saved as {chat_id}')

def load_phase(update, context):
    global phase
    phase = 'load'
    chat_id = update.effective_chat.id
    f = open(str(chat_id), 'r')
    ip_list = get_ip_list(chat_id)
    ip = f.readline()[:-1]
    while ip:
        print(ip)
        ip_list.append(ip)
        ip = f.readline()[:-1]
    f.close()
    send_message_to(chat_id, 'load complete')
    show_phase(update,context)

def run_monitor(update, context):
    global phase
    phase = 'run_monitor'
    chat_id = update.effective_chat.id
    save_phase(update,context)
    os.system(f'bash -c "exec -a {chat_id} python3 monitor.py {chat_id} &"')
    send_message_to(chat_id, 'Start monitoring successfully')

def stop_monitor(update, context):
    global phase
    phase = 'stop_monitor'
    chat_id = update.effective_chat.id
    os.system(f'pkill -f {chat_id}')
    send_message_to(chat_id, 'Stop monitoring successfully')

def print_help(update, context):
    message = update.message or update.edited_message
    msg = 'command list:\n\
            /add  : add new ip\n\
            /rm   : remove ip\n\
            /show : show ip list\n\
            /save : save current ip list\n\
            /load : load saved ip list\n\
            /run: start monitoring the ip\n\
            /stop : stop monitoring\n\
            /help : show the command list'
    message.reply_text(msg)
    check_and_add_chat_id(update.effective_chat.id)

def add_new_ip(chat_id, msg):
    ip_list = get_ip_list(chat_id)
    try:
        ip = str(re.search(IPv4_re, msg).group())
        if not ip in ip_list:
            ip_list.append(ip)
        send_message_to(chat_id, f'add {ip} successfully')
    except AttributeError:
        send_message_to(chat_id, f'add failed: ip not found')
        
def remove_ip(chat_id, msg):
    ip_list = get_ip_list(chat_id)
    try:
        ip = str(re.search(IPv4_re, msg).group())
        if ip in ip_list:
            ip_list.pop(ip_list.index(ip))
        send_message_to(chat_id, f'remove {ip} successfully')
    except AttributeError:
        send_message_to(chat_id, f'failed: ip not found')

def send_message_to(user_id='', msg=''):
    global bot
    bot.send_message(chat_id=user_id, text=msg)

def update_chat_id_list(chat_id=''):
    f = open('chat_id_list', 'r')
    chat_id_list = f.read().split('\n')
    f.close()
    chat_id_list.append(chat_id)
    f = open('chat_id_list', 'w')
    for chat_id in set(chat_id_list):
        f.write(str(chat_id) + '\n')
    f.close()

def responseHandler(update, context):
    global phase
    message = update.message or update.edited_message
    chat_id = update.effective_chat.id
    chat_input = message.text
    if chat_input == 'N':
        phase = ''
    elif phase == 'add':
        add_new_ip(chat_id, chat_input)
    elif phase == 'rm':
        remove_ip(chat_id, chat_input)

if __name__ == '__main__':
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('add', add_phase))
    updater.dispatcher.add_handler(CommandHandler('rm', rm_phase))
    updater.dispatcher.add_handler(CommandHandler('show', show_phase))
    updater.dispatcher.add_handler(CommandHandler('save', save_phase))
    updater.dispatcher.add_handler(CommandHandler('load', load_phase))
    updater.dispatcher.add_handler(CommandHandler('run', run_monitor))
    updater.dispatcher.add_handler(CommandHandler('stop', stop_monitor))
    updater.dispatcher.add_handler(CommandHandler('help', print_help))
    updater.dispatcher.add_handler(CommandHandler('start', print_help))
    dp.add_handler(MessageHandler(Filters.text, responseHandler))
    updater.start_polling()
    updater.idle()