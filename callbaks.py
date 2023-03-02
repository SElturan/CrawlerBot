from aiogram import types
from keyboards import get_keyboard
from api import bot
from base import post_subscribe, get_subscribe
from datetime import datetime, date


async def handle_callback(callback_query: types.CallbackQuery):
    category = None
    data = callback_query.data

    if data == "categories":
       
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = "Выберите категорию заявок", reply_markup=get_keyboard('categories'))

    elif data in ["WEB-разработка", "Обмен валют", "MARKETPLACES"]:
        # Сохраняем выбранную категорию заявки в переменную
        category = data
    
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Вы выбрали категорию заявки '{category}'.\n\nЧтобы получать заявки вам нужно приобрести подписку✅\n\nТакже вы можете приобрести бесплатную подписку на 3 дня", reply_markup=get_keyboard('subscribe'))
        
    

    elif data == "direct":
        user_id = callback_query.message.chat.id
        subs = await get_subscribe(user_id)
        keywords = []
        for sub in subs:
            if sub:
                keywords.append(sub["keyword"])

        if keywords:
            categories_text = " | ".join(keywords)

            end_dates_text = "\n".join(
                f"Подписка на <b>{keyword}</b> закончится в: <b>{datetime.strptime(sub['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d.%m.%Y')}</b>\nосталось дней: <b>{(datetime.strptime(sub['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.now()).days}</b>\n\n"
                for keyword, sub in zip(keywords, subs))

            message_text = f"Вы купили подписку на категории: \n<b>{categories_text}</b>\n\n{end_dates_text}"
        else:
            message_text = "У вас нет активных подписок"

        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message_text, reply_markup=get_keyboard('start'), parse_mode='HTML')


    elif data == "free":
        category = callback_query.message.text
        user_id = callback_query.message.chat.id
        category = callback_query.message.text  
        category_name = category.split("'")[1]


 

        data =  {
            "user_id": user_id,
            "keyword": category_name
        
        }

        sub_post = await post_subscribe(data)
       

        if sub_post:
            if category_name == 'WEB-разработка':
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: https://t.me/proleadsitebot')
            elif category_name == 'Обмен валют':
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: https://t.me/proleadcurrencybot')
            elif category_name == 'MARKETPLACES':
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: https://t.me/proleadmarketplacesbot')

            await callback_query.message.answer(f"Главное меню\n\nВыберите действие:", reply_markup=get_keyboard('start'))

        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = f"Вы уже приобрели пробную подписку на категорию {category_name}", reply_markup=get_keyboard('start'))


    elif data == "subscribe":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = "Выберите длительность подписки", reply_markup=get_keyboard('duration'))

    elif data in ['1', '14', '30', '90', '180']:
        # duration = data
        # category = callback_query.message.text
        # user_id = callback_query.message.chat.id

        # for categories in category:
        #     if categories in 'WEB-разработка':
        #         categorys = "WEB-разработка"
        #     elif categories in 'Обмен валют':
        #         categorys = "Обмен валют"
        #     elif categories in 'MARKETPLACES':
        #         categorys = "MARKETPLACES"

        # data = {
        #     "user_id": user_id,
        #     "keyword": categorys,
        #     "duration": int(duration)


        # }

        # post_sub = await post_subscribe(data)
        # if post_sub:
        #     await callback_query.message.answer(f"Вы успешно приобрели подписку на категорию {category}!", reply_markup=get_keyboard('start'))
        # else:
        #     await callback_query.message.answer(f"Вы уже приобрели подписку на категорию на {duration}!", reply_markup=get_keyboard('start'))
        await callback_query.message.answer(f"Платная версия пока недоступна.\n\nПользуйтесь пока бесплатной версией. с Уважанием PRO LEAD!", reply_markup=get_keyboard('start'))



    elif data == "back":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Главное меню\n\nВыберите действие:", reply_markup=get_keyboard('start'))

    