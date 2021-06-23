from celery import Celery

from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetMessagesRequest
import logging
import redis
import json
import requests

from services.textParser import emanuelefilter, transform_text, pasig
from services.signalProcessor import cleanOrderData


from teleredis import RedisSession
import redis
import json
from config import api_hash, api_id, REDISTOGO_URL
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
celery = Celery('tasks', broker= "redis://localhost")

url = "http://0.0.0.0:6061/response/messages/webhook"
request_url = "http://0.0.0.0:6061/request/messages/webhook"

headers = {'content-type': 'application/json'}


r = redis.from_url(url=REDISTOGO_URL)


@celery.task
def copytrade(session, channel_input, channel_output, phone):
        

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
        clean_text = text
        text = str(json.dumps(text))
        #text = '/historytotal'
        print("printing text after processing",text)
        #response = requests.post(url, data=json.dumps(event), headers=headers)
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
                    res_text = event.message.text
                    print(event.message)
                    response_data = {"phone":phone, "message":event.message.text }
                    response = requests.post(request_url, data=json.dumps(response_data), headers=headers)
                    
                    print(f"\u001b[32mSENT......{text}....SENT\u001b[37m....")
                except Exception as e:
                    print(e)
                    print(f"\u001b[31mNot Sent an error occurred {text[:70]} ...Not Sent\u001b[37m...") 

                
            else:
                print(f"\u001b[31mNot Sent invalid {text[:70]} ...Not Sent\u001b[37m...") 
    
    @client.on(
        events.NewMessage(
            chats= channel_output, 
            # pattern=r"^(BUY|SELL)\s([A-Z]*)\s[\(@at\s]*([0-9]*[.,][0-9]*)[\).]", 
            incoming=True,
            outgoing=True
            ))
    async def receivemessage(event):
        receive_text = event.message.text
        receive_data = {"message":receive_text, "phone":phone}
        response = requests.post(url, data=json.dumps(receive_data), headers=headers)

    @client.on(events.NewMessage)
    async def wakeup(event):
        print('..')

    client.start()
    #client.disconnect()
    # sleep(1)
    client.run_until_disconnected()
    #client.disconnect()
