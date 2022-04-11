#!/usr/bin/env python3
#-*-python-*-

import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
# from aiogram.utils.exceptions import Throttled

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from filters import setup_filters, IsNotCommand
from handlers import init_default_handlers
from states import UserStates, not_processing_state
from keyboards import KEYBOARDS
from logger import setup_logger

import json
from websocket import create_connection


HOST = '86.50.168.81'
PORT = 8080
TOKEN = os.environ['OPUSMT_TELEGRAMBOT_TOKEN']
LANG_DICT = {'English': 'en', 'Finnish': 'fi', 'French': 'fr', 'German': 'de', 'Swedish': 'sv', 'Ukrainian': 'uk'}

# PRE init
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
# setup filters
setup_filters(dp)
# setup default handlers
init_default_handlers(dp)

@dp.errors_handler()
async def global_error_handler(update, exception):
    logger.error(f'Update: {update} \n{exception}')

@dp.message_handler(state=not_processing_state, commands=['start'])
async def start_message(message: types.Message, state: FSMContext):
    await UserStates.start.set()
    await state.update_data(lang='en')
    await message.answer(
        "Hi! I'm an OPUS Translator bot. The default target language is English. Please press /lang if you'd like to choose some other.",
        reply_markup=KEYBOARDS['hide']
    )

@dp.message_handler(state='*', commands=['lang'])
async def help_message(message: types.Message, state: FSMContext):
    await UserStates.choose_lang.set()
    await message.answer(
        "Please, choose the target language.",
        reply_markup=KEYBOARDS['lang']['markup']
    )


@dp.message_handler(IsNotCommand(), state=UserStates.processing)
async def processing_message(message: types.Message, state: FSMContext):
    await message.answer('Please, wait for the previous text to be translated first!')


@dp.message_handler(IsNotCommand(), state=UserStates.choose_lang, content_types=['text'])
async def choose_lang(message: types.Message, state: FSMContext):
    lang = message.text.strip()
    if lang not in KEYBOARDS['lang']['options']:
        await message.answer('This language is not available')
        return
    lang = LANG_DICT[lang]
    await state.update_data(lang=lang)

    await message.answer('Thank you. You can print the sentence you\'d like to translate.', reply_markup=KEYBOARDS['hide'])
    await UserStates.start.set()


@dp.message_handler(IsNotCommand(), state=UserStates.start)
async def processing_message(message: types.Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    await UserStates.processing.set()
    await translate(text, message, target = data['lang'])
    await UserStates.start.set()


async def translate(text, message, host=HOST, port=PORT, source='detect', target='en'):
    ws = create_connection("ws://{}:{}/translate".format(host, port))
    data = {'text': text, 'source': source, 'target': target, 'model': 'default'}
    ws.send(json.dumps(data))
    result = ws.recv()
    record = json.loads(result)
    ws.close()
    await message.answer(record['result'])

async def on_startup(dispatcher):
    # do smth
    print('start')
    
async def on_shutdown(dispatcher):
    # do smth
    print('shutdown')

if __name__ == "__main__":
    filehandler_name = 'test_bot.log'
    logger = setup_logger(filehandler_name)
    # auth
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
