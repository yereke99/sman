#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from load import bot, dp
from aiogram import types
from FormaAdmin import *
from keyboard import*
from database import*
from config import*
from Forma import*
import asyncio
from traits import*
import time
from FormaAdmin import*
from aiogram.types import InputMediaPhoto, InputMediaVideo
from ChatForma import User_admin_mapping
from ChatForma import *




generator = Generator()
btn = Button()
db = Database()

@dp.message_handler(commands=['start', 'go'])
async def start_handler(message: types.Message):
    print(message.from_user.id)
      
    from datetime import datetime
    #fileId = "AgACAgIAAxkBAANcZwwL-emYUtwEKC8tOLtMa93tOnMAAqfoMRtMEGBILbrCi2y-dy4BAAMCAAN5AAM2BA"

    #user_id = message.from_user.id
    #user_name = f"@{message.from_user.username}"
    #time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #db.JustInsert(user_id, user_name, time_now)  
    
    await bot.send_message(
        message.from_user.id,
        text="""Добро пожаловать в FavPlaces! Здесь вы можете добавлять заведения и получать баллы для скидочной карты. Введите команду или используйте меню для действий.""",
        parse_mode="Markdown",
        reply_markup=btn.menu()
    )


# 🔍 Посмотреть мои заведения
@dp.message_handler(commands=['chat'])
@dp.message_handler(Text(equals="🔍 Чат с оператором"), content_types=['text'])
async def handler(message: types.Message):
    
    await Chat.waiting_for_message.set()

    await message.answer("Напишите сообщение оператору.", reply_markup=types.ReplyKeyboardRemove())

# Обработчик сообщений от пользователя
@dp.message_handler()
async def handle_user_message(message: types.Message):
    user_id = message.from_user.id
    user_info = f"@{message.from_user.username}" if message.from_user.username else message.from_user.full_name
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Связаться с пользователем", callback_data=f"contact_user:{user_id}"))
    
    await bot.send_message(admin2, f"Новое сообщение от пользователя {user_info}:\n{message.text}", reply_markup=keyboard)

    await message.answer("Сообщение отправлено оператору. Ожидайте ответа.")

# Обработчик нажатия Inline-кнопки
@dp.callback_query_handler(Text(startswith='contact_user:'))
async def process_contact_user_callback(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split(':')[1])
    admin_id = callback_query.from_user.id
    
    User_admin_mapping[admin_id] = user_id
    
    await bot.send_message(admin_id, f"Отправьте сообщение для пользователя {user_id}:")
    await bot.answer_callback_query(callback_query.id)


# Обработчик сообщений от администратора
@dp.message_handler(lambda message: message.from_user.id == admin2)
async def handle_admin_message(message: types.Message):
    admin_id = message.from_user.id
    user_id = User_admin_mapping.get(admin_id)
    
    if user_id:
        await bot.send_message(user_id, f"Сообщение от оператора:\n{message.text}")
    else:
        await message.reply("Используйте кнопку 'Связаться с пользователем' для начала диалога.")
