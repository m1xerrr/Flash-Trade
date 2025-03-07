﻿import Storage
import Listener
import API_Client as API
from Parser import TelegramListener
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import asyncio

API_TOKEN = "7995798682:AAGhVu4qVodVt5bhEGrN_xsiDjYKDxUVHc4"

bot = Bot(API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

Storage.init_db()

class SettingsState(StatesGroup):
    waiting_for_settings = State()

@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.reply("Welcome! Use /history, /channels, /settings, or other commands to interact with the bot.")

@dp.message(Command('history'))
async def history_command(message: types.Message):
    history = API.get_trade_history()
    if not history:
        await message.reply("⚠️ *No trade history found.*")
        return

    formatted_history = []
    for trade in history:
        status_emoji = "🟢" if trade["is_success"] else "🔴"
        formatted_trade = (
            f"{status_emoji} *Trade ID:* `{trade['id']}`\n"
            f"📅 *Date:* _{trade['created_at']}_\n"
            f"🪙 *Mint:* `{trade['mint']}`\n"
            f"🔗 *Tx Hash:* `{trade['tx_hash'] if trade['tx_hash'] != '-' else 'N/A'}`\n"
        )
        if not trade["is_success"]:
            formatted_trade += f"❌ *Error:* {trade['error'][:40]}...\n"

        formatted_history.append(formatted_trade)

    text = "\n\n".join(formatted_history)
    await message.reply(text)

@dp.message(Command('channels'))
async def channels_command(message: types.Message):
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
    if channels:
        channel_list = "\n".join(f"{idx + 1}. {channel}" for idx, channel in enumerate(channels))
        text = f"Channel list:\n{channel_list}"
    else:
        text = "The channel list is empty."
        
    await message.reply(text)

@dp.message(Command('settings'))
async def settings_command(message: types.Message):
    settings = API.get_auth_params()
    entry_price = settings.get("sol_lamports") / 1000000000
    slippage = settings.get("slippage") / 100
    text = (f"Current Settings:\n"
            f"Trade Amount (SOL): {entry_price}\n"
            f"Slippage (%): {slippage}\n")

    button = InlineKeyboardButton(text="Change Settings", callback_data="change_settings")
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

    await message.reply(text, reply_markup=markup)

@dp.callback_query(lambda c: c.data == 'change_settings')
async def change_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.reply(
        "Please enter the trade amount (SOL) and slippage (%) separated by a space (e.g., 1.5 0.5)."
    )
    await state.set_state(SettingsState.waiting_for_settings)

@dp.message(SettingsState.waiting_for_settings)
async def receive_settings(message: types.Message, state: FSMContext):
    try:
        trade_amount, slippage = message.text.split()
        trade_amount = float(trade_amount)
        slippage = float(slippage)

        if trade_amount <= 0 or slippage <= 0:
            raise ValueError("Values must be positive.")

        response = API.edit_auth_params(trade_amount * 1000000000, slippage * 100)

        if response is None:
            await message.reply("Invalid input. Please enter the trade amount and slippage as two positive numbers separated by a space.")
            return
        if response.find("success") is None:
            await message.reply("Invalid input. Please enter the trade amount and slippage as two positive numbers separated by a space.")
        else:
            await message.reply("Success")
            await state.clear()
    except ValueError:
        await message.reply("Invalid input. Please enter the trade amount and slippage as two positive numbers separated by a space.")

@dp.message()
async def fallback_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:  
        await message.reply("Unrecognized input. Please use a valid command.")

async def main():
    await Listener.initialize_listeners()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print(f'Program started at {datetime.now()}')
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f'Program finished at {datetime.now()}')
