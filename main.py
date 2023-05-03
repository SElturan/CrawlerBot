from aiogram import Bot, types
from aiogram import executor
from handlers.api import dp
from handlers.callbaks import handle_callback
from handlers.keyboards import get_keyboard
from handlers.base import user_get, user_post, get_admin
from handlers.text import *


class BotMain:
    def __init__(self, bot: Bot):
        self.bot = bot
        dp.register_message_handler(self.start, commands=['start', 'help', 'admin', ])
        dp.register_callback_query_handler(self.callback, lambda c: c.data in ['categories', 'back', 'Обмен валют', 'WEB-разработка', 'MARKETPLACES','direct', 'free','subscribe','duration','mailing_list','add_channels','aleksei','maria','ira','7', '14', '30', '90', '180'])



    async def start(self, message: types.Message):
        if message.text == '/start':
            first_name = message.from_user.first_name
            user_name = message.from_user.username
            user_id = message.from_user.id
            look_user_get = await user_get(user_id)

            data = {
                    "first_name": first_name,
                    "user_name": user_name,
                    "user_id": user_id
                    }
            
            if look_user_get:
                text = text_start()

                await message.answer(text=text, reply_markup=get_keyboard('start'))
        
            else:
                res = await user_post(data)
                text = text_start()

                if res:
                    await message.answer(text=text, reply_markup=get_keyboard('start'))
                else:
                    await message.answer('Ошибка, попробуйте позже!')

        elif message.text == '/admin':
            user_admin = message.from_user.id
            look_user_admin = await get_admin(user_admin)

            if look_user_admin:
                await message.answer('Добрый день администратор!\n\nВыберите действие"', reply_markup=get_keyboard('admin') ) 

            else:
                await message.answer('Вы не администратор!', reply_markup=get_keyboard('start'))


    async def callback(self, callback_query: types.CallbackQuery):
        await handle_callback(callback_query)



    





if __name__ == '__main__':
    BotMain(dp)
    executor.start_polling(dp, skip_updates=True)

