import sys
import logging
import asyncio

from aiogram.client.default import DefaultBotProperties
from pytonconnect import TonConnect
from connector import get_connector

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.handlers.transactions import send_transaction
from src.handlers.wallet import disconnect_wallet, connect_wallet
from src.loader import TOKEN

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    chat_id = message.chat.id
    connector = get_connector(chat_id)
    connected = await connector.restore_connection()

    mk_b = InlineKeyboardBuilder()
    if connected:
        mk_b.button(text='Send Transaction', callback_data='send_tr')
        mk_b.button(text='Disconnect', callback_data='disconnect')
        await message.answer(text='You are already connected!', reply_markup=mk_b.as_markup())

    else:
        wallets_list = TonConnect.get_wallets()
        for wallet in wallets_list:
            mk_b.button(text=wallet['name'], callback_data=f'connect:{wallet["name"]}')
        mk_b.adjust(1, )
        await message.answer(text='Choose wallet to connect', reply_markup=mk_b.as_markup())


@dp.callback_query(lambda call: True)
async def main_callback_handler(call: CallbackQuery):
    await call.answer()
    message = call.message
    data = call.data
    if data == "start":
        await command_start_handler(message)
    elif data == "send_tr":
        await send_transaction(message)
    elif data == 'disconnect':
        await disconnect_wallet(message)
    else:
        data = data.split(':')
        if data[0] == 'connect':
            await connect_wallet(message, data[1])


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)  # skip_updates = True
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
