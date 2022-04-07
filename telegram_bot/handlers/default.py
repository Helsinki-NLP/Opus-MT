from aiogram import types
from aiogram.dispatcher import FSMContext

async def get_id_message(message):
    uid = message.from_user.id
    await message.answer(str(uid))
    

async def get_state_message(message: types.Message, state: FSMContext):
    uid = message.chat.id
    state = await state.get_state()
    await message.answer(str(state))
