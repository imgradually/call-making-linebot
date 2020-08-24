from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import time
import psycopg2
import flex
import mylib
from datetime import datetime
import pytz
import constant
#from dbModel import *
app = Flask(__name__)

# Channel Access Token
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)
# Channel Secret
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
handler = WebhookHandler(channel_secret)
DATABASE_URL = os.getenv('DATABASE_URL', None)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#twilio
@app.route('/response', methods=['POST'])
def outbound():
    status = request.values.get('CallStatus')
    # lion_id = mylib.SQL_fetch(DATABASE_URL,"SELECT user_id FROM user_info where user_name='Lion'")
    # line_bot_api.push_message(to=lion_id,messages=TextSendMessage(text=status))
    print('Status: {}'.format(status))
    if status.lower() == 'completed':
        print("call completed")
    return ('', 204)

def make_call(user_name):
    user_phone = mylib.SQL_fetch(DATABASE_URL,"SELECT user_phone_number FROM user_info WHERE user_name='" + user_name + "'")
    if not user_phone:
        line_bot_api.push_message(to=to_id, messages=TextSendMessage(text="user phone not found"))
    else:
        mylib.call(phone=user_phone)
    return None

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    time = int(event.timestamp)/1000
    time += 28800 # tpe = pytz.timezone('Asia/Taipei')
    print(time)
    print(datetime.fromtimestamp(time).strftime('Now: %Y-%m-%d %H:%M:%S'))
    Now_hour = int(datetime.fromtimestamp(time).strftime('%H'))
    senderID = event.source.user_id
    Input_message = event.message.text.split()
    #testing_group_id = mylib.SQL_fetch(DATABASE_URL,"SELECT group_id FROM group_info where group_name='test'")
    tmp_message = ' '
    all_user_id = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT user_id FROM user_info")
    all_user_name = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT user_name FROM user_info")
    all_admin_id = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT admin_id FROM admin_info")
    all_group_id = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT group_id FROM group_info")
    if senderID in all_admin_id and event.message.text[0:3].lower() == 'sql':
        mylib.SQL(DATABASE_URL,event.message.text[4:])
        tmp_message = "SQL made successfully"
    elif event.message.text.lower() == 'my status':
        if senderID in all_admin_id:
            tmp_message = "you are admin"
        elif senderID in all_user_id:
            tmp_message = "you are user"
        else:
            tmp_message = "you are not registered yet"
    elif event.message.text.lower() == 'help': tmp_message = constant.Help_message_for_admin
    elif Input_message[0].lower() == 'echo': tmp_message = event.message.text[5:]
    elif event.message.text.lower() == 'hi' or event.message.text.lower() == 'hello':
        tmp_message = mylib.SQL_fetch(DATABASE_URL,"SELECT value FROM variable WHERE var_name='greeting'")
    elif event.message.text[0:6].lower() == 'change':
        SQL_order = "UPDATE variable SET value = '" + event.message.text[7:] + "' WHERE var_name='greeting'"
        mylib.SQL(DATABASE_URL,SQL_order)
        tmp_message = 'Greeting is changed to \n' + event.message.text[7:]
    elif Input_message[0].lower() == 'show':
        if Input_message[1].lower() == 'pid':
            tmp_message = 'Your ID is \n' + senderID 
        elif Input_message[1].lower() == 'gid':
            if hasattr(event.source, 'group_id'):
                tmp_message = 'Your group ID is \n' + event.source.group_id
            else:
                tmp_message = 'This is not a group.'
        elif Input_message[1].lower() == 'users' or Input_message[1].lower() == 'user':
            tmp_message = mylib.SQL_fetch(DATABASE_URL,"SELECT user_name FROM user_info")
        elif Input_message[1].lower() == 'groups'or Input_message[1].lower() == 'group':
            tmp_message = mylib.SQL_fetch(DATABASE_URL,"SELECT group_name,group_tag FROM group_info")
    elif Input_message[0].lower() == 'add':
        if hasattr(event.source, 'group_id') and event.source.group_id in all_it_group_id:
            if Input_message[3][0] != '+':
                tmp_message = "phone number should start with Country Calling Code (+886)"
            elif Input_message[2] in all_user_name:
                tmp_message = "The user name have already existed"
            elif (senderID in all_admin_id) or (senderID not in all_user_id):
                SQL_order = "INSERT INTO user_info (user_name,user_id,user_phone_number) VALUES ('"+Input_message[2]+"','"+senderID+"','"+Input_message[3]+"')"
                mylib.SQL(DATABASE_URL,SQL_order)
                tmp_message = "The user is added successfully"
            else:
                tmp_message = "You have already create your account"
        elif Input_message[1].lower() == 'group':
            all_group_name = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT group_name FROM group_info")
            if len(Input_message)<4:
                tmp_message = "請輸入:add group {group_name} {IT/CC}"
            elif hasattr(event.source, 'group_id'):
                acceptable_tag = ['IT','CC']
                if Input_message[2] in all_group_name:
                    tmp_message = 'The group name have already existed'
                elif Input_message[3] in acceptable_tag:
                    SQL_order = "INSERT INTO group_info (group_name,group_id,group_tag) VALUES ('"+Input_message[2]+"','"+event.source.group_id+"','"+Input_message[3]+"')"
                    mylib.SQL(DATABASE_URL,SQL_order)
                    tmp_message = 'The group is added successfully'
                else:
                    tmp_message = 'Unacceptable tag. Should be IT or CC'
            else:
                tmp_message = 'This is not a group.'
        elif Input_message[1].lower() == 'admin':
            new_admin_id = mylib.SQL_fetch(DATABASE_URL,"SELECT user_id FROM user_info WHERE user_name='" + Input_message[2].lower() + "'")
            if new_admin_id:
                mylib.SQL(DATABASE_URL,"INSERT INTO admin_info (admin_name,admin_id) VALUES ('"+Input_message[2]+"','"+new_admin_id+"')")
                tmp_message = 'Admin is added successfully'
            else:
                tmp_message = 'User not found'
    elif Input_message[0].lower() == 'delete' and Input_message[1].lower() == 'myself':
        if senderID in all_user_id:
            mylib.SQL(DATABASE_URL,"DELETE FROM user_info WHERE user_id='" + senderID + "'")
            tmp_message = "User deleted"
        else:
            tmp_message = "You are not user."
    elif Input_message[0].lower() == 'delete':
        if Input_message[1].lower() == 'user':
            if Input_message[2] in all_user_name:
                SQL_order = "DELETE FROM user_info WHERE user_name='" + Input_message[2] + "'"
                mylib.SQL(DATABASE_URL,SQL_order)
                tmp_message = "The user is deleted successfully"
            else:
                tmp_message = "The user does not exist"
        elif Input_message[1].lower() == 'group':
            all_group_name = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT group_name FROM group_info")
            if Input_message[2] in all_group_name:
                SQL_order = "DELETE FROM group_info WHERE group_name='" + Input_message[2] + "'"
                mylib.SQL(DATABASE_URL,SQL_order)
                tmp_message = "The group is deleted successfully"
            else:
                tmp_message = "The group does not exist"
        elif senderID == lion_id and Input_message[1].lower() == 'admin':
            all_admin_name = mylib.SQL_fetch_arr(DATABASE_URL,"SELECT admin_name FROM admin_info")
            if Input_message[2] in all_admin_name:
                SQL_order = "DELETE FROM admin_info WHERE group_name='" + Input_message[2] + "'"
                mylib.SQL(DATABASE_URL,SQL_order)
                tmp_message = "The admin is deleted successfully"
            else:
                tmp_message = "The admin does not exist"
    elif Input_message[0].lower() == 'search':
        if Input_message[1].lower() == 'user':
            SQL_order = "SELECT user_phone_number FROM user_info WHERE user_name='" + Input_message[2] + "'"
            tmp_message = mylib.SQL_fetch(DATABASE_URL,SQL_order)
            if tmp_message:
                tmp_message = "The user's phone number is\n" + tmp_message
            else:
                tmp_message = "The user does not exist"
    elif Input_message[0].lower() == 'call':
        if Input_message[1] in all_user_name:
            make_call(Input_message[1])
    if tmp_message == ' ':
            tmp_message = 'Command Error\nCommand: help'
    tmp_message += "\n" + datetime.fromtimestamp(time).strftime('Message recieved time (UTC+8):\n %Y-%m-%d %H:%M:%S')
    message = TextSendMessage(text=tmp_message)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_postback(event):
    Input_message = event.postback.data.split()
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="postback recieved:\n"+event.postback.data))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)