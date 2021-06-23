from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetMessagesRequest
import logging
import redis
from backend.models import User
from services.textParser import emanuelefilter, transform_text, pasig
from services.signalProcessor import cleanOrderData
from datetime import datetime   
from config import api_hash, api_id, REDISTOGO_URL
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

r = redis.from_url(url=REDISTOGO_URL)
channel_output = ["@MT4RobotTradingbot"]
channel_input = []



     
client = TelegramClient("marc", api_id, api_hash)

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
    text = str(text)
    #text = '/historytotal'
    print("printing text after processing",text)

    
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
            except Exception as e:
                print(e)
                print(f"\u001b[31mNot Sent an error occurred {text[:70]} ...Not Sent\u001b[37m...") 

            
        else:
            print(f"\u001b[31mNot Sent invalid {text[:70]} ...Not Sent\u001b[37m...") 

@client.on(events.NewMessage)
async def wakeup(event):
    print('..')

client.start()
client.run_until_disconnected()
