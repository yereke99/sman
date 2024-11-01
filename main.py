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
      
    from datetime import datetime
    #fileId = "AgACAgIAAxkBAANcZwwL-emYUtwEKC8tOLtMa93tOnMAAqfoMRtMEGBILbrCi2y-dy4BAAMCAAN5AAM2BA"

    user_id = message.from_user.id
    user_name = f"@{message.from_user.username}"
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db.JustInsert(user_id, user_name, time_now)  
    
    await bot.send_message(
        message.from_user.id,
        text=f"Сәлеметсіз бе, {message.from_user.first_name}! 👋\n"
            """SMAN - премиум Қазақ бренді. 

4 мемлекетте тігіледі 🇵🇹🇨🇳🇹🇷🇮🇹

200 ерлер мен әйелдерге әлемнің қаймақтарын алып келеміз

No pig leather""",
        parse_mode="Markdown",
        reply_markup=btn.menu()
    )


"""
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
    
"""


# 🔍 Посмотреть мои заведения
@dp.message_handler(commands=['chat'])
@dp.message_handler(Text(equals="🗣 Менеджермен байланыс"), content_types=['text'])
async def handler(message: types.Message):
    
    await Chat.waiting_for_message.set()

    await message.answer("Напишите сообщение оператору.", reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id

    # Основное меню
    if data == "buy_shoes":
        # Показать выбор категории обуви с удалением предыдущего сообщения
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз аяқ киім сатып алғыңыз келеді. Төменнен санатты таңдаңыз:",
            reply_markup=btn.category_selection_keyboard()
        )

    elif data == "contact_manager":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Менеджермен байланысу үшін: /chat командасын басыңыз"
        )

    elif data == "my_orders":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Бұл жерде сіздің тапсырыстарыңыз көрсетіледі."
        )

    elif data == "about_us":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="SMAN - жоғары сапалы итальяндық аяқ киім дүкені. Қош келдіңіз!",
            reply_markup=btn.webInsta()
        )

    # Обработка выбора категории обуви
    elif data == "category_men":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз ерлер аяқ киімін таңдадыңыз. Түрін таңдаңыз:",
            reply_markup=btn.men_shoes_keyboard()
        )
    
    elif data == "category_women":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз әйелдер аяқ киімін таңдадыңыз. Түрін таңдаңыз:",
            reply_markup=btn.women_shoes_keyboard()
        )

    # Обработка кнопки "Назад" для категорий и возврата в главное меню
    elif data == "back_to_menu":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Басты мәзірге оралдыңыз:",
            reply_markup=btn.menu()
        )

    elif data == "back_to_category":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Санатты қайта таңдаңыз:",
            reply_markup=btn.category_selection_keyboard()
        )

    # Обработка выбора типа мужской обуви
    elif data == "men_sneakers":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Ерлер кроссовкилары және кедылар. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "men_boots":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Ерлер бәтеңкелері. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "men_boots_high":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Ерлер етігі. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "men_shoes":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Ерлер туфлиі. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )

    # Обработка выбора типа женской обуви
    elif data == "women_sneakers":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Әйелдер кроссовкилары және кедылар. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "women_boots":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Әйелдер бәтеңкелері. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "women_boots_high":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Әйелдер етігі. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )
    elif data == "women_shoes":
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Сіз таңдадыңыз: Әйелдер туфлиі. Жақын арада тауарды Telegram ботта онлайн түрде рәсімдей аласыз."
        )

    # Ответ для callback_query
    await bot.answer_callback_query(callback_query.id)




