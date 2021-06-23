from collections import namedtuple
from flask import Flask,jsonify
from sqlalchemy.orm import session
from config import DevelopmentConfig
from db import db
from flask_restx import Api,fields
from views.views import api as userNS
from views.views import api2 as authNSpip
from views.views import api4 as apiNSS
from views.views import api5 as apiNSSS

from backend.models import User, Inputs

from views.views import Register, Login, ChatInput, ChatOutput
import configparser
import json
from flask import request
from time import sleep
from services import dbresource
# from main import copytrade
from flask_cors import CORS

from config import api_hash, api_id

from telethon.sessions import StringSession
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from flask_socketio import SocketIO



from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetMessagesRequest
import logging
import redis
import json
import requests

from telemongo import MongoSession

import time

from teleredis import RedisSession
import redis
import asyncio

from flask import request
from services.textParser import emanuelefilter, transform_text, pasig
from services.signalProcessor import cleanOrderData
from datetime import datetime
from backend.models import User, Inputs
from services import dbresource

import pymongo

from flask_pymongo import PyMongo
import flask


from config import api_hash, api_id, REDISTOGO_URL
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


from mongoengine import connect

DEFAULT_CONNECTION_NAME = connect('blog')

headers = {'content-type': 'application/json'}


import datetime
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
CORS(app)



api = Api(app, version = "1.0", 
		  title = "ProfitSnipper BybitBot Api", 
		  description = "Admin panel",
          doc="/docs")

# adding the namespaces
api.add_namespace(userNS, path='/users')
api.add_namespace(apiNSS)
api.add_namespace(apiNSSS)
api.add_namespace(authNSpip)

url = "http://0.0.0.0:5051/response/messages/webhook"
request_url = "http://0.0.0.0:5051/request/messages/webhook"

headers = {'content-type': 'application/json'}

api_id = 4154197
api_hash = "17b0517fd71fbff8674d4b43169207a0"


#phone number verification
@app.route('/auth/verify/mobile', methods=['POST'])
async def auth_phone():
    phone = request.json['phone']
    email = request.json['email']
    
    records = db.session.query(User).filter_by(email = email).first()
    if records:
        username = records.username
    
        client = TelegramClient(username, api_id, api_hash)
        await client.connect()

        print("connected==============")

        response = {'code_sent': False}

        if not await client.is_user_authorized():
            await client.send_code_request("+{}".format(phone))
            response['code_sent'] = True

        return {"message": "Verification code sent", "status": 200}


    else:
        return {"message": "user does not exist", "status": 400}

    
@app.route('/auth/verify/code', methods=['POST'])
async def auth_code():
    code = request.json['code']
    phone = request.json['phone']
    email = request.json['email']
    
    records = db.session.query(User).filter_by(email = email).first()
    if records:
        username = records.username

        client = TelegramClient(username, api_id, api_hash)
        #client.start()    
        await client.connect()
        print("connected========================")

        if not await client.is_user_authorized():
            await client.send_code_request("+{}".format(phone))
            await client.sign_in(phone, code)

        response = {'logged_in': False}

        if await client.is_user_authorized():
            response['logged_in'] = True
            
        return {"message": "Logged in successfully", "status": 200}


    else:
        return {"message": "user does not exist", "status": 400}


@app.route('/stringsession', methods=['POST'])
async def stringsession():
    email = request.json['email']
    
    records = db.session.query(User).filter_by(email = email).first()
    if records:
        username = records.username

    async with TelegramClient(username, api_id, api_hash) as client:
        string_session = StringSession.save(client.session)
        db.session.query(User).filter_by(email=email).update({'session':string_session})
        db.session.commit()


        return {"message":"session saved successfully", "status": 200}


@app.route('/groups/channels', methods=['GET'])
async def get_entity_data():
    email = request.json['email']
    session = dbresource.getSession(email)
    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.connect()

    result = await client(GetDialogsRequest(
             offset_date=None,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=100,
             hash=0)) 

    entities = result.chats
    print("---------------", entities)
    channel_store = []
    for entity in entities:
        ent = {
            "id": entity.id,
            "title": entity.title
        }
        print("---------------", ent)
        channel_store.append(ent)
    print("--------------------", channel_store)
    
    return {"data":channel_store}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
    