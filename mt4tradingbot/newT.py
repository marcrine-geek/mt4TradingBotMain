from requests.sessions import session
from telemongo import MongoSession
from telethon import TelegramClient
from flask import request
from telethon import client
from telethon.client import auth
from backend.models import User, CodeData
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from db import db
from pyrogram import Client, methods
import time
from typing import Union, List, Optional
from pyrogram.storage import Storage, FileStorage, MemoryStorage
from pyrogram.methods.auth.connect import Connect
from pyrogram.types import User, TermsOfService
from pyrogram.errors import (
    SessionPasswordNeeded,
    VolumeLocNotFound, ChannelPrivate,
    AuthBytesInvalid, BadRequest
)


from flask import Flask
from flask_mongoengine import MongoEngine
import pymongo

from flask_pymongo import PyMongo
import flask
import time

from pyrogram.connection import Connection
from pyrogram.raw.core import TLObject, MsgContainer, Int, FutureSalt, FutureSalts
from pyrogram.raw.all import layer
from pyrogram.errors import RPCError, InternalServerError, AuthKeyDuplicated, FloodWait


import logging
from pyrogram.raw.core import TLObject


from pyrogram import raw
from pyrogram import types
from pyrogram.errors import PhoneMigrate, NetworkMigrate
from pyrogram.session import Session, Auth
from config import DevelopmentConfig


log = logging.getLogger(__name__)

app = flask.Flask(__name__)
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

api_id = 49631
api_hash = "fb050b8f6771e15bfda5df2409931569"


template = """
UserBot support: @marcrine
            
<code>STRING_SESSION</code>: <code>{}</code>

⚠️ <b>Please be carefull to pass this value to third parties</b>"""


class Records(Client):
    def __init__(self, session_name: Union[str, Storage],api_id: Union[int, str] = None,api_hash: str = None, phone_number: str = None,phone_code: str = None):

        super().__init__(session_name, api_id, api_hash, phone_number, phone_code)

    def __enter__(self):
        return self.start()

    
    async def start(self):
        print("starting client")
        while True:
            self.connection = Connection(
                self.dc_id,
                self.test_mode,
                self.client.ipv6,
                self.client.proxy
            )

            try:
                await self.connection.connect()

                self.network_task = self.loop.create_task(self.network_worker())

                self.current_salt = FutureSalt(0, 0, Session.INITIAL_SALT)
                self.current_salt = FutureSalt(
                    0, 0,
                    (await self._send(
                        raw.functions.Ping(ping_id=0),
                        timeout=self.START_TIMEOUT
                    )).new_server_salt
                )
                self.current_salt = (await self._send(
                    raw.functions.GetFutureSalts(num=1),
                    timeout=self.START_TIMEOUT)).salts[0]

                self.next_salt_task = self.loop.create_task(self.next_salt_worker())

                if not self.is_cdn:
                    await self._send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=self.client.api_id,
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",
                                query=raw.functions.help.GetConfig(),
                            )
                        ),
                        timeout=self.START_TIMEOUT
                    )

                self.ping_task = self.loop.create_task(self.ping_worker())

                log.info(f"Session initialized: Layer {layer}")
                log.info(f"Device: {self.client.device_model} - {self.client.app_version}")
                log.info(f"System: {self.client.system_version} ({self.client.lang_code.upper()})")

            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, TimeoutError, RPCError):
                await self.stop()
            except Exception as e:
                await self.stop()
                raise e
            else:
                break

        self.is_connected.set()

        log.info("Session started")


    async def connect(self) -> bool:
        
        print("client connecting")
        if self.is_connected:
            raise ConnectionError("Client is already connected")

        self.load_config()
        await self.load_session()
        print("printing something")

        self.session = Session(
            self, await self.storage.dc_id(),
            await self.storage.auth_key(), await self.storage.test_mode()
        )

        await self.session.start()

        self.is_connected = True

        return bool(await self.storage.user_id())


    async def send(
        self,
        data: TLObject,
        retries: int = Session.MAX_RETRIES,
        timeout: float = Session.WAIT_TIMEOUT,
        sleep_threshold: float = None
    ):
        print("sending...")
        
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if self.no_updates:
            data = raw.functions.InvokeWithoutUpdates(query=data)

        if self.takeout_id:
            data = raw.functions.InvokeWithTakeout(takeout_id=self.takeout_id, query=data)

        r = await self.session.send(
            data, retries, timeout,
            (sleep_threshold
             if sleep_threshold is not None
             else self.sleep_threshold)
        )

        await self.fetch_peers(getattr(r, "users", []))
        await self.fetch_peers(getattr(r, "chats", []))

        return r


    async def send_code(self, phone_number: str) -> "types.SentCode":
        phone_number = phone_number.strip(" +")
        print("printing phone in library", phone_number)
        await Records.connect(self)
        while True:
            try:
                print("==================phone number", phone_number)

                r = await self.send(
                    raw.functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=raw.types.CodeSettings()
                    )
                )
                print("===============printing r", r)
            except (PhoneMigrate, NetworkMigrate) as e:
                await self.session.stop()

                await self.storage.dc_id(e.x)
                await self.storage.auth_key(
                    await Auth(
                        self, await self.storage.dc_id(),
                        await self.storage.test_mode()
                    ).create()
                )
                self.session = Session(
                    self, await self.storage.dc_id(),
                    await self.storage.auth_key(), await self.storage.test_mode()
                )

                await self.session.start()
            else:
                return types.SentCode._parse(r)


    async def authorize(self, phone_number, phone_code) -> User:
        self.phone_number = phone_number
        self.phone_code = phone_code
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        while True:
            try:
                print("++++++++++++++", self.phone_number)
                sent_code = await self.send_code(self.phone_number)
                print("======================", sent_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        if self.force_sms:
            sent_code = await self.resend_code(self.phone_number, sent_code.phone_code_hash)

        print("The confirmation code has been sent via {}".format(
            {
                "app": "Telegram app",
                "sms": "SMS",
                "call": "phone call",
                "flash_call": "phone flash call"
            }[sent_code.type]
        ))

        print("phone_code_hash=====", sent_code.phone_code_hash)
        while True:
            if self.phone_code:
                self.phone_code = phone_code
                input("enter code----------: ")

            try:
                print("signing in ---------------")

                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
                print("signed in user...")
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None

            else:
                break
    




@app.route('/auth/verify/mobile', methods=['POST'])
async def auth_phone():
    phone = request.json['phone']
    record = Records(session_name=phone, api_id=api_id, api_hash=api_hash, phone_number=phone)
    print("--------------")
    
    await record.authorize(phone_number=phone)

    return "successfully sent code"


@app.route('/auth/verify/code/<phone>', methods=['POST'])
async def auth_code(phone):
    code = request.json['code']

    record = Records(session_name=phone, api_id=api_id, api_hash=api_hash, phone_number=phone, phone_code=code)


    await record.authorize(phone_number=phone, phone_code=code)

    with record(phone, api_id, api_hash) as pyrogram:
        saved_messages_template = "Pyrogram session" + template.format(pyrogram.export_session_string())
        print("\nGenerating String session...\n")           
        pyrogram.send_message("me", saved_messages_template, parse_mode="html")
        time.sleep(1) 
        print("Your STRING_SESSION value have been sent to your Telegram Saved Messages")


    return "successfully sent session"



@app.route('/groups/channels/<phone>', methods=['GET'])
async def get_entity_data(phone):
    print("==============================")
    
    client = TelegramClient(phone, api_id, api_hash)
    #client.start()    
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
    
    await client.disconnect()
    return {"data":channel_store}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)



# db.createUser(
#   {
#     user: "copytrading",
#     pwd: "copytrading",
#     roles: [ { role: "read", db: "mt4tradingbot" } ]
#   }
# )

# db.createUser({ user: "copytrading" , pwd: "copytrading", roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]})