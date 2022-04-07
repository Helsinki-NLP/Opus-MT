# from contextvars import ContextVar
from aiogram import types
from aiogram.types import CallbackQuery, ChatType, InlineQuery, Message, Poll, ChatMemberUpdated
from aiogram.dispatcher.filters import Filter, BoundFilter

    
class IsNotCommand(Filter):
    key = 'not_command'

    async def check(self, message: types.Message):
        return not message.text.startswith('/')
