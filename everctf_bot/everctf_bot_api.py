import json
from flask import Flask, request, jsonify
from telegram import *
from telegram.ext import *
from everctf_bot_data import token

def send_message_to(chat_id, msg):
    bot = Bot(token)
    bot.send_message(chat_id=chat_id, text=msg)

def get_chat_id_list():
    f = open('chat_id_list', 'r')
    chat_id_list = f.read()[:-1].split('\n')
    f.close()
    return set(chat_id_list)

app = Flask(__name__)

@app.route('/broadcast', methods=['POST'])
def broadcast():
    post_data = json.loads(request.data)
    chat_id_list = get_chat_id_list()
    print(chat_id_list)
    for chat_id in chat_id_list:
        send_message_to(chat_id, post_data['message'])
    return(jsonify("send complete"))

app.run(debug=True)