import re
import asyncio
import Channel
import API_Client as API
from telethon import TelegramClient
from telethon.tl.types import Message
from datetime import datetime, timezone


class TelegramListener:
    SOLANA_CONTRACT_PATTERN = r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b'

    def __init__(self, channel_username, api_id='2576129', api_hash='0f54c8a4b6ee6cb8025e10b208199873', update_interval=5):
        self.api_id = api_id
        self.api_hash = api_hash
        self.channel_username = channel_username
        self.update_interval = update_interval
        self.last_message_date = datetime.now(timezone.utc)
        self.session_name = f"session_{channel_username.strip('@')}"
        self.addresses = [] 

    def process_message(self, message):
        if message.text:
            sanitized_text = re.sub(r'[\'"|()|{}[\]\\/@#$%^&*<>?!~`+=]', ' ', message.text)
            words = sanitized_text.split()

            for word in words:
                if len(word) > 44:
                    sub_words = word.split('/')
                    for sub_word in sub_words:
                        if 32 <= len(sub_word) <= 44 and re.fullmatch(self.SOLANA_CONTRACT_PATTERN, sub_word):
                            self.save_address(sub_word, message.date)
                            return
                elif 32 <= len(word) <= 44 and re.fullmatch(self.SOLANA_CONTRACT_PATTERN, word):
                    API.perform_swap(word)
                    Channel.send_message(f'New address found {word} at {self.channel_username} [{message.date}]')
                    return

    def save_address(self, address, message_date):
        self.addresses.append({
            'channel': self.channel_username,
            'address': address,
            'datetime': message_date
        })
        print(f"[Saved Solana Contract] {address} at {message_date}")

    async def start(self):
        async with TelegramClient(self.session_name, self.api_id, self.api_hash) as client:
            try:
                channel = await client.get_entity(self.channel_username)
                print(f"Listening to Telegram channel: {self.channel_username}")

                while True:
                    new_last_message_date = None

                    async for message in client.iter_messages(channel, limit=1):
                        if message and message.date > self.last_message_date:
                            new_last_message_date = message.date

                    if new_last_message_date:
                        async for message in client.iter_messages(channel):
                            if isinstance(message, Message) and message.date:
                                if message.date > self.last_message_date:
                                    self.process_message(message)
                                else:
                                    break

                        self.last_message_date = new_last_message_date

                    print(f"Waiting for {self.update_interval / 60} minutes...")
                    await asyncio.sleep(self.update_interval)

            except Exception as e:
                print(f"An error occurred: {e}")
