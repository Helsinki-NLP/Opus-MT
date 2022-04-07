from aiogram import Dispatcher

from .filters import IsNotCommand


def setup_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsNotCommand)