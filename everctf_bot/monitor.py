from telegram import *
from telegram.ext import *
import sys
import os
import time
from everctf_bot_data import token

bot = Bot(token)

def send_message_to(chat_id, msg):
    global bot
    bot.send_message(chat_id=chat_id, text=msg)

def read_ip_list(chat_id):
    f = open(str(chat_id), 'r')
    ip_list = []
    ip = f.readline()[:-1]
    while ip:
        print(ip)
        ip_list.append(ip)
        ip = f.readline()[:-1]
    f.close()
    return ip_list

if __name__ == '__main__':
    chat_id = sys.argv[1]
    ip_list = read_ip_list(chat_id)
    while True:
        for ip in ip_list:
            port = ''
            command = f'ping -c 3 -w 5 {ip.split(":")[0]}'
            if ip.find(":") >= 0:
                command = f'ping -c 3 -w 5 {ip.split(":")[0]} -p {ip.split(":")[1]}'
            ret_code = os.system(command)
            if not ret_code == 0:
                send_message_to(chat_id, f'can not ping to ip {ip}')
        time.sleep(60)