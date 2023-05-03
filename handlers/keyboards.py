
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests

from config import http_api


def get_keyboard(name: str, flag: bool = False):
    if name == 'start':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Категория заявок 📩', callback_data='categories'))
        if not flag:
            keyboard.add(InlineKeyboardButton(text='Личный кабинет 👤', callback_data='direct'))
        keyboard.add(InlineKeyboardButton(text='Тех.Поддержка 🖥️', url='https://t.me/botasoft'))
    
    elif name == 'direct':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Пополнить счет', callback_data='duration'))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))
        
    elif name == 'categories':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        req = requests.get (f"{http_api}/keywordcategories/")
        for keyword in req.json():
            keyboard.add(InlineKeyboardButton(keyword['name'], callback_data=str(keyword['name'])))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))

    elif name == 'subscribe':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        if flag:
            keyboard.add(InlineKeyboardButton(text='Продлить подписку ⏳', callback_data='duration'))
            keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))
        else:
            keyboard.add(InlineKeyboardButton(text='3 дн. бесплатно', callback_data='free'))
            keyboard.add(InlineKeyboardButton(text='Приобрести подписку ✅', callback_data='subscribe'))
    
    elif name == 'duration':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='1 неделя', callback_data= '7' ))
        keyboard.add(InlineKeyboardButton(text='2 недели', callback_data='14'))
        keyboard.add(InlineKeyboardButton(text='1 месяц', callback_data='30'))
        keyboard.add(InlineKeyboardButton(text='3 месяца', callback_data='90'))
        keyboard.add(InlineKeyboardButton(text='6 месяцев', callback_data='180'))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))
    
    elif name == 'admin':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='➕Добавить каналы', callback_data='add_channels'))
        keyboard.add(InlineKeyboardButton(text='📨Сделать рассылку', callback_data='mailing_list'))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))

    elif name == 'agent':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Алексей(Сайты)🌐', callback_data='aleksei'))
        keyboard.add(InlineKeyboardButton(text='Зинаида(Маркетплейсы)⚡️', callback_data='maria'))
        keyboard.add(InlineKeyboardButton(text='Петя(Обмен валют)💸', callback_data='ira'))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))

    elif name == 'url':
        keyboard = InlineKeyboardMarkup(resize_keyboard=True)
        keyboard.add(InlineKeyboardButton(text='Отправьте заявку сюда', url='https://t.me/botasoft'))
        keyboard.add(InlineKeyboardButton(text='Назад🔙', callback_data='back'))


    return keyboard
        


