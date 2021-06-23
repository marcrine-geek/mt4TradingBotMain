from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from flask import Flask
import asyncio
import sys
import time
import asyncio
#import aiohttp

import os
import asyncio
import sys
import time
import socks
from telethon import TelegramClient, events, utils
from flask import request
from telethon.sessions import StringSession


app = Flask(__name__)

# @app.route("/", methods=["POST"])
# async def get_data():
#     data = await async_db_query(...)
#     return jsonify(data)
# session = "marcrine"
# api_hash = "f9f30bd7582c2425a19999b6c5fbd439"
# api_id = 4215361
# proxy = socks.SOCKS5, '', 1080
# # Create and start the client so we can make requests (we don't here)

# print("________________________________")
# client = TelegramClient(session, api_id, api_hash, proxy=proxy).start()
# client = TelegramClient("jojj2", api_id, api_hash)

# async def main():
#     # Now you can use all client methods listed below, like for example...
#     await client.send_message('me', 'Hello to myself!')

# with client:
#     client.loop.run_until_complete(main())

api_id = 4215361
api_hash = "f9f30bd7582c2425a19999b6c5fbd439"

@app.route('/auth/<phone>', methods=['POST'])
async def auth_phone(phone):
    client = TelegramClient("my_name", api_id, api_hash, proxy=("socks5", '127.0.0.1', 4444))
    await client.connect()

    response = {'code_sent': False}

    if not await client.is_user_authorized():
        await client.send_code_request("+{}".format(phone))
        response['code_sent'] = True

    return {"message":"success"}

@app.route('/auth/<phone>/<code>', methods=['POST'])
async def auth_code(phone, code):
    client = TelegramClient("my_name", api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request("+{}".format(phone))
        await client.sign_in(phone, code)

    response = {'logged_in': False}

    if await client.is_user_authorized():
        response['logged_in'] = True

    return "great"



if __name__ == '__main__':
    app.run()