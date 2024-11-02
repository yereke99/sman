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


# Запуск функции отправки сообщения при старте бота
@dp.message_handler(commands=["s1"])
async def start_handler(message: types.Message):
    await send_product_to_channel()
    await message.answer("Товар успешно отправлен в канал.")

@dp.message_handler(commands=["s2"])
async def start_handler(message: types.Message):
    await send_product_to_channel2()
    await message.answer("Товар успешно отправлен в канал.")

@dp.message_handler(commands=["s3"])
async def start_handler(message: types.Message):
    await send_product_to_channel3()
    await message.answer("Товар успешно отправлен в канал.")




async def send_product_to_channel():
    # Идентификатор канала
    channel_id = "@sman_online"

    # Данные товара
    product_name = "Лофер GIAMPIERONICOLA"
    price = "157 000 KZT"
    size = "Размер: 40"
    color = "Цвет: синий"
    code = "Код: MN19/24-1"
    text = f"{product_name}\nЦена: {price}\n{size}\n{color}\n{code}"

    # Ссылка на бота
    bot_username = "smanonline_bot"
    bot_url = f"https://t.me/{bot_username}?start=buy_product_MN19_24_1"

    # Создание Inline-кнопки "Сатып алу"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сатып алу", url=bot_url))

    # Отправка сообщения с фото товара, описанием и кнопкой в канал
    await bot.send_photo(
        chat_id=channel_id,
        photo="https://sman.kz/upload/resize_cache/iblock/840/450_450_140cd750bba9870f18aada2478b24840a/nkblq0co5dr7z3loc1qvvfro4uuqd88o.jpg",  # Ссылка на фото товара или загрузите локальный файл
        caption=text,
        reply_markup=keyboard
    )



async def send_product_to_channel2():
    # Идентификатор канала
    channel_id = "@sman_online"

    # Данные товара
    product_name = "Мужские кроссовки"
    price = "157 000 KZT"
    size = "Размер: 42"
    stock = "В наличии: 5 пар"
    text = f"{product_name}\nЦена: {price}\n{size}\n{stock}"

    # Ссылка на бота
    bot_username = "smanonline_bot"
    bot_url = f"https://t.me/{bot_username}?start=buy_product"

    # Создание Inline-кнопки "Сатып алу"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сатып алу", url=bot_url))

    # Отправка сообщения с фото товара, описанием и кнопкой в канал
    await bot.send_photo(
        chat_id=channel_id,
        photo="https://sman.kz/upload/resize_cache/iblock/bff/450_450_140cd750bba9870f18aada2478b24840a/6fbzu6308pskqaf2755w9aiuxzbvkzh0.jpg",  # Ссылка на фото товара или загрузите локальный файл
        caption=text,
        reply_markup=keyboard
    )

async def send_product_to_channel3():
    # Идентификатор канала
    channel_id = "@sman_online"

    # Данные товара
    product_name = "Лофер GIAMPIERONICOLA"
    price = "157 000 KZT"
    size = "Размер: 39"
    color = "Цвет: черный"
    code = "Код: MN24/24-1"
    text = f"{product_name}\nЦена: {price}\n{size}\n{color}\n{code}"

    # Ссылка на бота
    bot_username = "smanonline_bot"
    bot_url = f"https://t.me/{bot_username}?start=buy_product_MN24_24_1"

    # Создание Inline-кнопки "Сатып алу"
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Сатып алу", url=bot_url))

    # Отправка сообщения с фото товара, описанием и кнопкой в канал
    await bot.send_photo(
        chat_id=channel_id,
        photo="https://sman.kz/upload/resize_cache/iblock/b9f/450_450_140cd750bba9870f18aada2478b24840a/vapke21k1n4bhl85bv2vtyu1vo7dthc6.jpg",  # Новое фото товара
        caption=text,
        reply_markup=keyboard
    )



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
        
    # Обработка связи с пользователем
    elif data.startswith("contact_user:"):
        user_id = int(data.split(':')[1])
        print(f"Связь с пользователем {user_id}")
        
        async with state.proxy() as state_data:
            state_data['user_id'] = user_id

        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Отправьте сообщение для пользователя {user_id}:"
        )
        await Chat.sending_for_message.set()

    # Ответ для callback_query
    await bot.answer_callback_query(callback_query.id)




