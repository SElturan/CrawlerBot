from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.dispatcher import FSMContext 
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from enum import Enum
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from handlers.base import get_agents,get_keyword_categories,get_active_kyword, get_active_sub
from config import *


memory_storage = MemoryStorage()

bot = Bot(token=TOKEN_MARKET)
dp = Dispatcher(bot, storage=memory_storage)

class States(Enum):
    STARTED = 1


@dp.message_handler(commands=("start"))
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    
    current_state = await state.get_state()
    if current_state is not None:
        # Если стейт уже был записан, значит пользователь уже запускал бота
        return
    
    keyword = 'MARKETPLACES'
    get_sub = await get_active_sub(user_id, keyword)

    if get_sub:
        await message.answer("Бот активирован, скоро вы начнёте получать первые заявки")
        await state.set_state(States.STARTED)
        return
    else:

        await message.answer("Бот не может быть активирован, так как у вас не оплачена категория.\nПодробнее: @prolead_bot")
        await state.set_state(States.STARTED)


@dp.message_handler()
async def new_message(message: types.Message):

    agent_id = 6268914430

    if message.chat.id == agent_id:


        keywords='MARKETPLACES'

        get_sub = await get_active_kyword(keywords)

        for user_id in get_sub:

            try:
                
                await bot.forward_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)

            except Exception:
                continue


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)




