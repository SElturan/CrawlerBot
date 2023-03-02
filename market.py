
import telethon.tl.types
from aiogram import Bot, Dispatcher, types
from aiogram import executor
import datetime


from base import get_agents, user_get, get_users, get_keyword_categories, get_subscribe, get_subscribe_id, get_subscribes

from config import *

from keyboards import *
import pytz



bot = Bot(token=TOKEN_MARKET)
dp = Dispatcher(bot)


async def on_startup(_):
    users_id = await get_users()

    for user_id in users_id:
        try:
            await bot.send_message(chat_id=user_id, text="⚡️ ВЕДУТСЯ ТЕХНИЧЕСКИЕ РАБОТЫ. Приносим извинения. Время простоя будет добавлено в ваши приобретенные периоды.\n\nЗакончили обновлять бота, заявки начнут приходить в прежнем режиме.\nНе забудьте нажать /start чтобы получать свежие заявки")
        except Exception:
            continue



@dp.message_handler(commands='start')
async def start_money(message: types.Message):
    
    user_id = message.from_user.id
    look_user_get = await user_get(user_id)
    subs = await get_subscribe(user_id)
  


    
    if  look_user_get:

        if subs:
            
            web_subs = [sub for sub in subs if sub["keyword"] == "MARKETPLACES"]
            if not web_subs:
                await message.answer("Чтобы активировать бота вам нужно купить подписку\nhttps://t.me/prolead_bot")
                return
            
            else:
                web_sub = web_subs[0]
                end_date = datetime.datetime.fromisoformat(web_sub["end_date"].replace('Z', '+00:00')).replace(tzinfo=pytz.UTC)
                now = datetime.datetime.now(pytz.UTC)

                if end_date < now:
                    await message.answer("Ваша подписка закончилась.Чтобы продлить подписку перейдите по ссылке\nhttps://t.me/prolead_bot")
                    return
                else:

                    await get_users()

                    await message.answer("Вы активировали бота.Скоро будете получать первые заявки")

                    
                    @dp.message_handler()
                    async def new_message(message: types.Message):
   
                        agent_id = await get_agents()

                        

                        if message.chat.id in agent_id:
                            if message.text.startswith('[AGENT]'):
                                user_admin = message.from_user.id
                                look_user_admin = await user_get(user_admin)
                                if look_user_admin[0]['is_admin'] == True:
                                    agent_username = message.from_user.username
                                    if agent_username is None:
                                        agent_username = message.from_user.first_name + " " + message.from_user.last_name
                                    text = message.text.replace('AGENT', f'AGENT @{agent_username}')
                                    await bot.send_message(chat_id=look_user_admin, text=text)
                                return

                            


                            subs = await get_subscribes()
                            unique_users = set(user['user_id'] for user in subs if user['keyword'] == 'MARKETPLACES')
                            


                            for sub in unique_users:
                                
                                get_kw = await get_keyword_categories()
                                web_subs = [sub for sub in subs if sub["keyword"] == "MARKETPLACES"]
                                if not web_subs:
                                    continue
                                else:
                                    web_sub = web_subs[0]
                         
                                    end_date = datetime.datetime.fromisoformat(web_sub["end_date"].replace('Z', '+00:00')).replace(tzinfo=pytz.UTC)
                                    now = datetime.datetime.now(pytz.UTC)
                              
                                    if end_date < now:
                                        continue
                                    else:
                                        
                                        for kw in get_kw:
                                            if kw['name'] == 'MARKETPLACES':
                                                for keyword in kw['keywords']:
                                                    if keyword['keyword'].lower() in message.text.lower():
                                                    
                                                    
                                                        

                                                        await bot.forward_message(chat_id=sub, from_chat_id=message.chat.id, message_id=message.message_id)

                                                
                                                        break
                                            
                                            
                                            else:
                                                continue

    
        else:
            await message.answer("Чтобы активировать бота вам нужно купить подписку\nhttps://t.me/prolead_bot")

    else:
        await bot.send_message(message.chat.id, text="Чтобы активировать бота вам нужно купить подписку\nhttps://t.me/prolead_bot")






if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)











