from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import Message
from load import dp, bot
from aiogram import types 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import logging
from keyboard import*
from database import Database
import datetime
from main import*
import asyncio
from config import admin
from datetime import datetime
from traits import *
import time
from traits import*
from config import*
import os


User_admin_mapping = {} # {admin_message_id: user_id}

btn = Button()

class Chat(StatesGroup):
    waiting_for_message = State()



@dp.message_handler(state='*', commands='🔕 Бас тарту')
@dp.message_handler(Text(equals='🔕 Бас тарту', ignore_case=True), state='*')
async def cancell_handler(message: types.Message, state: FSMContext):
    """
    :param message: Бастартылды
    :param state: Тоқтату
    :return: finish
    """
    
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Бас тарту!')
    
    await state.finish()
    await message.reply('Сіз тапсырыстан бас тарттыңыз.', reply_markup=btn.menu())

@dp.message_handler(state=Chat.waiting_for_message, content_types=types.ContentType.ANY)
async def handle_user_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    # Получаем информацию о пользователе
    if message.from_user.username:
        user_info = f"@{message.from_user.username}"
    else:
        user_info = f"{message.from_user.full_name}"

    
    print(user_id)

    # Отправляем сообщение администратору в зависимости от типа контента
    if message.content_type == 'text':
        sent_message = await bot.send_message(
            chat_id=admin,
            text=f"Новое сообщение от пользователя {user_info}:\n{message.text}",
            reply_markup=btn.contact_user_button(user_id)
        )
    elif message.content_type == 'photo':
        sent_message = await bot.send_photo(
            chat_id=admin,
            photo=message.photo[-1].file_id,
            caption=f"Новое фото от пользователя {user_info}",
            reply_markup=btn.contact_user_button(user_id)
        )
    elif message.content_type == 'document':
        sent_message = await bot.send_document(
            chat_id=admin,
            document=message.document.file_id,
            caption=f"Новое сообщение от пользователя {user_info}",
            reply_markup=btn.contact_user_button(user_id)
        )
    else:
        # Для других типов контента
        sent_message = await bot.send_message(
            chat_id=admin,
            text=f"Новое сообщение от пользователя {user_info}: (тип контента: {message.content_type})",
            reply_markup=btn.contact_user_button(user_id)
        )
        await message.forward(admin)  # Пересылаем контент без reply_markup

    # Сохраняем соответствие между сообщением и user_id
    User_admin_mapping[sent_message.message_id] = user_id

    await message.answer("Сообщение отправлено оператору. Ожидайте ответа.")

    await state.finish()



    

