from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from datetime import datetime
from aiogram import types
from handlers.api import bot, dp
import asyncio
import pytz
from handlers.base import post_subscribe, get_active_subscriptions, get_check_sub, patch_sub, get_agents, add_channels, get_users
from handlers.text import text_sub_duration, text_sub_category
from handlers.keyboards import get_keyboard



async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    
    category_user = data


    if data == "categories":
       
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = "Выберите категорию заявок", reply_markup=get_keyboard('categories'))

    elif data in ["WEB-разработка", "Обмен валют", "MARKETPLACES"]:
        category = data
        context = {'category': category_user}
        await dp.current_state(chat=callback_query.message.chat.id, user=callback_query.message.from_user.id).update_data(context)
        await dp.current_state(chat=callback_query.message.chat.id, user=callback_query.message.from_user.id).set_state('category')

        user_id = callback_query.message.chat.id
        get_sub = await get_check_sub(user_id, category)

        if get_sub:
            markup = get_keyboard('subscribe', flag=True)
            text = text_sub_category(category)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=markup)
        
        else:
            markup = get_keyboard('subscribe')
            text = text_sub_category(category)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text, reply_markup=markup)
    

    elif data == "direct":
        user_id = callback_query.message.chat.id
        active_subscriptions = await get_active_subscriptions(user_id)

        if active_subscriptions:
            message = "Вы купили подписку на категории:\n\n"
            for sub in active_subscriptions:
                keyword = sub['keyword']
                end_date = datetime.fromisoformat(sub['end_date']).astimezone(pytz.utc).astimezone(pytz.timezone('Europe/Moscow'))
                days_left = (end_date - datetime.now(pytz.timezone('Europe/Moscow'))).days
                if days_left < 0:
                    days_left = '0 (категория заморожена)'
                
                message += f"<b>{keyword}</b>\n"
                message += f"Подписка на категорию <b>{keyword}</b> закончится в: <i>{end_date.strftime('%d.%m.%Y')}</i>\n"
                message += f"Осталось дней: <b>{days_left}</b>\n\n"
        else:
            message = "У вас нет активных подписок."

        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message, reply_markup=get_keyboard('start', flag=True), parse_mode='HTML')
        

    elif data == "free":
        user_id = callback_query.message.chat.id
        state = dp.current_state(chat=user_id, user=callback_query.message.from_user.id)
        category_context = await state.get_data()
        category_name = category_context.get('category')


        if category_context is None:
            # Категория заявок не выбрана, выведите сообщение об ошибке
            await bot.answer_callback_query(callback_query.id, text='Пожалуйста, сначала выберите категорию заявок.')
        else:
            
            data = {
                "user_id": user_id,
                "keyword": category_name
            }
            sub_post = await post_subscribe(data)

            if sub_post:
                if category_name == 'WEB-разработка':
                    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: @proleadsitebot')
                elif category_name == 'Обмен валют':
                    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: @proleadcurrencybot')
                elif category_name == 'MARKETPLACES':
                    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text='Перейдите в этого бота и нажмите запустить, он вам будет отправлять заявки: @proleadmarketplacesbot')

                await callback_query.message.answer(f"Главное меню\n\nВыберите действие:", reply_markup=get_keyboard('start'))

            else:
                await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=f"Вы уже приобрели пробную подписку на категорию {category_name}", reply_markup=get_keyboard('start'))


    elif data == "subscribe":
        user_id = callback_query.message.chat.id

        state = dp.current_state(chat=user_id, user=callback_query.message.from_user.id)
        category_context = await state.get_data()
       
        if category_context is None:
            # Категория заявок не выбрана, выведите сообщение об ошибке
            await bot.answer_callback_query(callback_query.id, text='Пожалуйста, сначала выберите категорию заявок.')

        else:
            category_name = category_context.get('category')

        text = text_sub_category(category_name)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = text, reply_markup=get_keyboard('duration'))

    elif data == "duration":


        user_id = callback_query.message.chat.id

        state = dp.current_state(chat=user_id, user=callback_query.message.from_user.id)
        category_context = await state.get_data()
        
        if category_context is None:
            # Категория заявок не выбрана, выведите сообщение об ошибке
            await bot.answer_callback_query(callback_query.id, text='Пожалуйста, сначала выберите категорию заявок.')

        else:
            category_name = category_context.get('category')

        text = text_sub_duration(category_name)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = text, reply_markup=get_keyboard('duration'))

    elif data in ['7', '14', '30', '90', '180']:

        text = 'Чтобы приобрести платную напишите условия ниже.\n\nНапишите название категории\nДлительность подписки\nИ ожидайте реквизит\n\n'
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = text, reply_markup=get_keyboard('url'))

        # duration = data

        # user_id = callback_query.message.chat.id

        # state = dp.current_state(chat=callback_query.message.chat.id, user=callback_query.message.from_user.id)
        # category_context = await state.get_state('category')

        # if category_context is None:
        #     # Категория заявок не выбрана, выведите сообщение об ошибке
        #     await bot.answer_callback_query(callback_query.id, text='Пожалуйста, сначала выберите категорию заявок.')

        # else:
        #     category_name = category_context.get('category')


        # get_sub = await get_check_sub(user_id, category_name)
        # if get_sub:
        #     id_user = get_sub[0]['id']
        #     patch_subscribe = await patch_sub(id_user, int(duration))
        #     if patch_subscribe:
        #         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = f"Вы успешно продлили подписку на категорию {category_name}\nДлительность подписки {duration} дней!", reply_markup=get_keyboard('start'))
            
        #     else:
        #         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = f"Оплата не прошла", reply_markup=get_keyboard('start'))


          
            

        # else:
        #     data_post =  {
        #         "user_id": user_id,
        #         "keyword": category_name,
        #         "duration": duration
        #     }

        #     sub_post = await post_subscribe(data_post)
        #     if sub_post:
        #         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = f"Вы успешно приобрели подписку на категорию {category_name}\nДлительность подписки {duration} дней!", reply_markup=get_keyboard('start'))

        #     else:
        #         await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text = f"Оплата не прошла", reply_markup=get_keyboard('start'))
            

    elif data == "back":
        await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text="Главное меню\n\nВыберите действие:", reply_markup=get_keyboard('start'))

    elif data == 'add_channels':
        
        await bot.edit_message_text(chat_id = callback_query.message.chat.id, message_id=callback_query.message.message_id, text= 'Выберите нишу',reply_markup=get_keyboard('agent'))
        
    elif data == 'aleksei':

        class Channels(StatesGroup):
            add_channels = State()


        await callback_query.message.answer('Введите ссылку на канал или группу')
        await Channels.add_channels.set()

        @dp.message_handler(state=Channels.add_channels)
        async def add_channel(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['add_channels'] = message.text
                

                await add_channels(message.text)
                
                await bot.send_message(6263981492, message.text)

                await state.finish()

                await asyncio.sleep(2)

                await callback_query.message.answer('Группа успешно отправлена агенту!', reply_markup=get_keyboard('admin'))

    elif data == 'ira':
        class ChannelsIra(StatesGroup):
            add_channels = State()


        await callback_query.message.answer('Введите ссылку на канал или группу')
        await ChannelsIra.add_channels.set()

        @dp.message_handler(state=ChannelsIra.add_channels)
        async def add_channel(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['add_channels'] = message.text
                

                await add_channels(message.text)
                
                await bot.send_message(6112482534, message.text)

                await state.finish()

                await asyncio.sleep(2)

                await callback_query.message.answer('Группа успешно отправлена агенту!', reply_markup=get_keyboard('admin'))

    elif data == 'maria':
        class ChannelsMari(StatesGroup):
            add_channels = State()


        await callback_query.message.answer('Введите ссылку на канал или группу')
        await ChannelsMari.add_channels.set()

        @dp.message_handler(state=ChannelsMari.add_channels)
        async def add_channel(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['add_channels'] = message.text
                

                await add_channels(message.text)
                
                await bot.send_message(6268914430, message.text)

                await state.finish()

                await asyncio.sleep(2)

                await callback_query.message.answer('Группа успешно отправлена агенту!', reply_markup=get_keyboard('admin'))



    elif data == 'mailing_list':
        class Channels(StatesGroup):
            messages = State()


        await callback_query.message.answer('Отправьте текст для рассылки')
        await Channels.messages.set()

        @dp.message_handler(state=Channels.messages)
        async def messages(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['messages'] = message.text
                

                await callback_query.message.answer('Отправляю всем вашу рассылку...')
                user = await get_users()
                for user_id in user:
                    try:

                        await bot.send_message(user_id, message.text)
                    except Exception:
                        continue

                    await state.finish()
                await asyncio.sleep(2)

                await callback_query.message.answer('Рассылка успешно отправлена!', reply_markup=get_keyboard('admin'))

                    

