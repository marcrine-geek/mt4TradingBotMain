from telegram.client import Telegram
code = 23451
tg = Telegram(
    api_id = 4154197,
    api_hash = "17b0517fd71fbff8674d4b43169207a0",
    phone='+254780827587',  # you can pass 'bot_token' instead
    database_encryption_key='changekey123',
)
tg.send_code(code)
tg.login()
print("---------------------------------")
# if this is the first run, library needs to preload all chats
# otherwise the message will not be sent
result = tg.get_chats()
result.wait()

# `tdlib` is asynchronous, so `python-telegram` always returns you an `AsyncResult` object.
# You can receive a result with the `wait` method of this object.
result.wait()
print(result.update)

tg.stop()  # you must call `stop` at the end of the script