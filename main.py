import telethon.tl.types
from aiogram import Bot, types
from keyboards import get_keyboard
from base import user_get, user_post,get_agents, add_channels
from aiogram import executor
from api import dp, bot
from callbaks import handle_callback
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup




class BotMain:
    def __init__(self, bot: Bot):
        self.bot = bot
        dp.register_message_handler(self.start, commands=['start', 'help', 'admin', 'add_channels'])
        dp.register_callback_query_handler(self.callback, lambda c: c.data in ['categories', 'back', 'Обмен валют', 'WEB-разработка', 'MARKETPLACES','direct', 'free','subscribe','7', '14', '30', '90', '180'])



    async def start(self, message: types.Message):
        if message.text == '/start':
            first_name = message.from_user.first_name
            user_name = message.from_user.username
            user_id = message.from_user.id
            print(user_id,'flfd;s')
            look_user_get = await user_get(user_id)
            # print(look_user_get)

            data = {
                    "first_name": first_name,
                    "user_name": user_name,
                    "user_id": user_id,
                    "is_admin": False,
                    "is_bot": False
                    }
            if look_user_get :
                res = await user_post(data)
                text = '''Приветствуем тебя в PRO LEAD! Круто, что ты теперь с нами 🤗

В этом боте мы собираем для тебя заявки из сотни бизнес-чатов в Telegram и ищем людей, нуждающихся в разных услугах: внж, обмен валют, недвижимость, создание сайтов, дизайн и т.д.

📍В разделе «Категория заявок» ты можешь выбрать нужную тебе категорию и попробовать ее в деле.

📍Нажав кнопку «Техподдержка», можно задать любой вопрос по работе бота.'''
                if res:
                    await message.answer(text=text, reply_markup=get_keyboard('start'))
                else:
                    await message.answer(text=text, reply_markup=get_keyboard('start'))
            else:
                res = await user_post(data)
                await message.answer('''Приветствуем тебя в PRO LEAD! Круто, что ты теперь с нами 🤗

В этом боте мы собираем для тебя заявки из сотни бизнес-чатов в Telegram и ищем людей, нуждающихся в разных услугах: внж, обмен валют, недвижимость, создание сайтов, дизайн и т.д.

📍В разделе «Категория заявок» ты можешь выбрать нужную тебе категорию и попробовать ее в деле.

📍Нажав кнопку «Техподдержка», можно задать любой вопрос по работе бота.''', reply_markup=get_keyboard('start'))

        elif message.text == '/admin':
            user_admin = message.from_user.id
            look_user_admin = await user_get(user_admin)
            if look_user_admin[0]['is_admin'] == True:
                await message.answer('Добрый день администратор!\nЧтобы добавить новые каналы нажмите на команду /add_channels')  

            else:
                await message.answer('Вы не администратор!', reply_markup=get_keyboard('start'))
        elif message.text == '/add_channels':
            user_admin = message.from_user.id
            look_user_admin = await user_get(user_admin)
            if look_user_admin[0]['is_admin'] == True:                   

                class Channels(StatesGroup):
                    add_channels = State()


                await message.answer('Введите ссылку на канал или группу')
                await Channels.add_channels.set()

                @dp.message_handler(state=Channels.add_channels)
                async def add_channel(message: types.Message, state: FSMContext):
                    async with state.proxy() as data:
                        data['add_channels'] = message.text
                       

                        await add_channels(message.text)
                        await message.answer('Вход в группы...')
                        agents = await get_agents()
                        for agent in agents:
                            await bot.send_message(agent, message.text)
                            await state.finish()

                    
    
            else:
                await message.answer('Вы не администратор!', reply_markup=get_keyboard('start'))


            

    async def callback(self, callback_query: types.CallbackQuery):
        await handle_callback(callback_query)

    





if __name__ == '__main__':
    BotMain(dp)
    executor.start_polling(dp, skip_updates=True)

