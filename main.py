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
from ChatForma import*




generator = Generator()
btn = Button()
db = Database()

@dp.message_handler(commands=['start', 'go'])
async def start_handler(message: types.Message):
    print(message.from_user.id)
      
    #from datetime import datetime
    #fileId = "AgACAgIAAxkBAANcZwwL-emYUtwEKC8tOLtMa93tOnMAAqfoMRtMEGBILbrCi2y-dy4BAAMCAAN5AAM2BA"

    #user_id = message.from_user.id
    #user_name = f"@{message.from_user.username}"
    #time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #db.JustInsert(user_id, user_name, time_now)  
    
    await bot.send_message(
        message.from_user.id,
        text="""Добрый день!""",
        parse_mode="Markdown",
        reply_markup=btn.menu()
    )

@dp.callback_query_handler(lambda call: call.data.startswith("contact_user:"))
async def callback_inline(call: types.CallbackQuery):
    print("INLINE")
    if call.data.startswith("contact_user:"):
        print("INLINE обработчик сработал")

        # Распарсим ID пользователя из callback данных
        user_id = call.data.split(":")[1]
        
        # Отправим сообщение, что inline-кнопка успешно обработана
        await bot.send_message(call.message.chat.id, f"Отправьте сообщение для пользователя {user_id}:")
        await call.answer()
    


# 🔍 Посмотреть мои заведения
@dp.message_handler(commands=['chat'])
@dp.message_handler(Text(equals="🔍 Чат с оператором"), content_types=['text'])
async def handler(message: types.Message):
    
    await Chat.waiting_for_message.set()

    await message.answer("Напишите сообщение оператору.", reply_markup=types.ReplyKeyboardRemove())



"""
# Обработчик нажатия Inline-кнопки
@dp.callback_query_handler()
async def process_contact_user_callback(callback_query: types.CallbackQuery):
    print("here")
    if callback_query.data.startswith("contact_user:"):
        user_id = int(callback_query.data.split(':')[1])
        print(user_id)
        admin_id = callback_query.from_user.id
        
        User_admin_mapping[admin_id] = user_id
        
        await bot.send_message(callback_query.message.chat.id, f"Отправьте сообщение для пользователя {user_id}:")
        await bot.answer_callback_query(callback_query.id)
"""




