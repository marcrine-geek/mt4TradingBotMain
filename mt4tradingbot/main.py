from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetMessagesRequest
import logging
import redis
import json
import requests

from flask import request
from services.textParser import emanuelefilter, transform_text, pasig
from services.signalProcessor import cleanOrderData
from datetime import datetime
from backend.models import User, Inputs 
from services import dbresource

from config import api_hash, api_id, REDISTOGO_URL
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
from celery import Celery


celery = Celery('tasks', broker= "redis://localhost")

# r = redis.from_url(url=REDISTOGO_URL)

url = "http://178.32.191.159:5050/messages/webhook"

headers = {'content-type': 'application/json'}

channel_output = []
channel_input = dbresource.chatInputs(user_id=User.id)

session = User.username

@celery.task
def copytrade(session, channel_input, channel_output):
        
    client = TelegramClient(StringSession(session), api_id, api_hash)

    @client.on(
        events.NewMessage(
            chats= channel_input, 
            # pattern=r"^(BUY|SELL)\s([A-Z]*)\s[\(@at\s]*([0-9]*[.,][0-9]*)[\).]", 
            incoming=True,
            outgoing=True
            ))
    async def forwarder(event):
        text = event.message.text
        message_id = event.message.id
        reply_msg = event.message.reply_to_msg_id
        print("printing text", text)
        valid = emanuelefilter(text)
        # text pasing
        # text = pasig(text)
        # text = transform_text(text)

        # sending processed data for testing
        text = cleanOrderData(text)
        
        text = str(json.dumps(text))
        #text = '/historytotal'
        print("printing text after processing",text)
        response = requests.post(url, data=json.dumps(event), headers=headers)
        count = 0
        for cht in channel_output:
            try:
                ref = int(r.get(f"{cht}-{reply_msg}").decode('utf-8'))
            except:
                print('Out of scope or bounds for redis')
                ref = None
            try:
                msg_file = event.message.file.media
                ext = event.message.file.ext
            except:
                msg_file = None
                ext = None

            count += 1
            print(cht, count)

            if valid:
                try:
                    output_channel = await client.send_message(cht, text, file=msg_file, reply_to=ref)
                    r.set(f"{cht}-{event.message.id}", output_channel.id)
                    # # sending processed data
                    # output_channel2 = await client.send_message(cht, text2, file=msg_file, reply_to=ref)
                    # r.set(f"{cht}-{event.message.id}", output_channel2.id)
            
                    print(f"\u001b[32mSENT......{text}....SENT\u001b[37m....")
                except:
                    print(f"\u001b[31mNot Sent an error occurred {text[:70]} ...Not Sent\u001b[37m...") 

                
            else:
                print(f"\u001b[31mNot Sent invalid {text[:70]} ...Not Sent\u001b[37m...") 

    @client.on(events.NewMessage)
    async def wakeup(event):
        print('..')

    client.start()
    client.run_until_disconnected()
