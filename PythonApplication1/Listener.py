from Parser import TelegramListener
import asyncio
import Storage

active_listeners = {}
active_tasks = {}

async def start_listener(channel_username):
    listener = TelegramListener(channel_username)
    task = asyncio.create_task(listener.start())
    active_listeners[channel_username] = listener
    active_tasks[channel_username] = task

async def stop_listener(channel_username):
    task = active_tasks.pop(channel_username, None)
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print(f"Listener for {channel_username} stopped.")

async def initialize_listeners():
    channels = [
    "@theholyz",
    "@ABOC100X",
    "@houseofdegeneracy",
    "@shahlito",
    "@PowsGemCalls",
    "@InDaTrenches",
    "@ProfitsPlays",
    "@CookersCooks",
    "@nft_brewery",
    "@constablecalls",
    ]
    for channel in channels:
        if channel not in active_tasks:
            await start_listener(channel)