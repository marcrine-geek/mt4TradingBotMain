from pyrogram import Client
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



# from backend.models import User

api_id = 49631
api_hash = "fb050b8f6771e15bfda5df2409931569"

template = """
UserBot support: @marcrine
            
<code>STRING_SESSION</code>: <code>{}</code>

⚠️ <b>Please be careful to pass this value to third parties</b>"""

class Records(Client):
    def __init__(self, session_name: Union[str, Storage],api_id: Union[int, str] = None,api_hash: str = None):
        super().__init__(session_name, api_id, api_hash)
    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = input("Enter phone number: ")
                        print("===========value", value)

                        if not value:
                            continue

                        confirm = (input(f'Is "{value}" correct? (y/N): ')).lower()

                        if confirm == "y":
                            break

                    if ":" in value:
                        self.bot_token = value
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value
                        print("+++++++++++++++++", self.phone_number)

                sent_code = await self.send_code(self.phone_number)
                print("================code sent", sent_code)
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

        while True:
            if not self.phone_code:
                self.phone_code = input("Enter code: ")

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await input("Enter password (empty to recover): ", hide=self.hide_password)

                    try:
                        if not self.password:
                            confirm = await input("Confirm password recovery (y/n): ")

                            if confirm == "y":
                                email_pattern = await self.send_recovery_code()
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await input("Enter recovery code: ")

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        log.error(e, exc_info=True)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break




with Records("usermarc", api_id, api_hash) as pyrogram:
    saved_messages_template = "Pyrogram session" + template.format(pyrogram.export_session_string())
    print("\nGenerating String session...\n")           
    pyrogram.send_message("me", saved_messages_template, parse_mode="html")
    time.sleep(1) 
    print("Your STRING_SESSION value have been sent to your Telegram Saved Messages")