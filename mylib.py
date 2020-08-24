import psycopg2
import os
from twilio.rest import Client
def SQL_fetch(DATABASE_URL,SQL_order):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(SQL_order)
    conn.commit()
    message = ''
    first = True
    while True:
        temp = cursor.fetchone()
        if temp:
            if first:
                if len(temp)==1:
                    message = message + str(temp[0])
                else:
                    message = message + str(temp)
                first = False
            else:
                if len(temp)==1:
                    message = message + '\n' + str(temp[0])
                else:
                    message = message + '\n' + str(temp)
        else:
            if first:
                message = None
                print('SQL_fetch empty')
            break
    cursor.close()
    conn.close()
    return message
def SQL(DATABASE_URL,SQL_order):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(SQL_order)
    conn.commit()
def SQL_fetch_arr(DATABASE_URL,SQL_order):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(SQL_order)
    conn.commit()
    data = []
    while True:
        temp = cursor.fetchone()
        if temp:
            if len(temp)==1: data.append(temp[0])
            else: data.append(temp)
        else:
            break
    cursor.close()
    conn.close()
    return data
account_sid = os.getenv('TWILIO_ACCOUNT_SID', None)
auth_token = os.getenv('TWILIO_AUTH_TOKEN', None)
def call(phone=None):
    client = Client(account_sid, auth_token)
    call = client.calls.create(
                            method='GET',
                            url='http://demo.twilio.com/docs/voice.xml',
                            to=phone,
                            from_='+15128430505',
                            status_callback='https://lionslinebot.herokuapp.com/response',
                            status_callback_event=['completed'],
                            status_callback_method='POST',
                            timeout=15
                        )