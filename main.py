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
#from Forma import*
import asyncio
from traits import*
import time
from FormaAdmin import*
from ChatForma import*
from data import SHOES_DATA
from Formas import*
import re
from mongo import*


generator = Generator()
btn = Button()
db = MongoDB()


"""
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
            SMAN - премиум Қазақ бренді. 

4 мемлекетте тігіледі 🇵🇹🇨🇳🇹🇷🇮🇹

200 ерлер мен әйелдерге әлемнің қаймақтарын алып келеміз

No pig leather,
        parse_mode="Markdown",
        reply_markup=btn.menu()
    )

"""

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message, state: FSMContext):
    args = message.get_args()

    if args.startswith("buy_"):
        product_code = args.replace("buy_", "")

        # Ищем товар в базе данных по коду
        product = db.getByCodeAllData(product_code)
        
        if product:
            category = product.get("category", "Тауар")
            price = product.get("discounted_price", "Белгісіз")
            sizes = product.get("sizes", [])
            initial_price = product.get("initial_price", price)

            # Сохраняем состояние и данные о товаре
            await state.update_data(type=product_code)
            await Forma.s3.set()  # Переход к следующему состоянию (Forma.s3)

            # Отправка информации о товаре пользователю с кнопками размеров
            await message.answer(
                f"Сіз {category} - {price} KZT тауарын таңдадыңыз.\n"
                f"❌ Алғашқы бағасы: {initial_price} тг\n"
                f"✅ Жаңа баға: {price} тг\n"
                f"📏 Қол жетімді өлшемдер: {', '.join(map(str, sizes))}\n"
                f"🔖 Код: {product_code}\n\n"
                "Өлшемді таңдау үшін төмендегі батырманы басыңыз.",
                reply_markup=btn.size_keyboard(sizes)  # Кнопки с размерами
            )
        else:
            # Если товар с данным кодом не найден
            await message.answer("Кешіріңіз, бұл код бойынша тауар табылмады.")
    else:
        await message.answer("Ботқа қош келдіңіз! Сатып алу үшін кодты таңдаңыз. @sman_online")

# Запуск функции отправки сообщения при старте бота
@dp.message_handler(commands=["m1"])
async def start_handler(message: types.Message):
    sex = "Ерлер"
    price = "37 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")


# Запуск функции отправки сообщения при старте бота
@dp.message_handler(commands=["m2"])
async def start_handler(message: types.Message):
    sex = "Ерлер"
    price = "27 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")

@dp.message_handler(commands=["m3"])
async def start_handler(message: types.Message):
    sex = "Ерлер"
    price = "57 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")

@dp.message_handler(commands=["m4"])
async def start_handler(message: types.Message):
    sex = "Ерлер"
    price = "17 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")



# Запуск функции отправки сообщения при старте бота
@dp.message_handler(commands=["w1"])
async def start_handler(message: types.Message):
    sex = "Әйелдер"
    price = "57 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")


# Запуск функции отправки сообщения при старте бота
@dp.message_handler(commands=["w2"])
async def start_handler(message: types.Message):
    sex = "Әйелдер"
    price = "37 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")

@dp.message_handler(commands=["w3"])
async def start_handler(message: types.Message):
    sex = "Әйелдер"
    price = "17 900"
    await send_product_to_channel(sex, price)
    await message.answer("Товар успешно отправлен в канал.")



@dp.message_handler(commands=["code"])
async def code_handler(message: types.Message):
    # Идентификатор канала
    channel_id = "@sman_online"  # Укажите ваш канал

    # Извлекаем код из сообщения
    args = message.text.split(" ", 1)  # Разделяем команду и аргумент
    if len(args) < 2:
        await message.reply("Код товара отсутствует. Используйте формат: /code <код товара>")
        return

    code = args[1].strip()
    product = db.getByCodeAllData(code)

    if product:
        # Извлекаем данные о товаре
        category = product.get("category", "Не указано")
        price = product.get("discounted_price", "Не указано")
        sizes = ", ".join(map(str, product.get("sizes", [])))
        file_id = product.get("file_id", None)

        # Формируем сообщение
        product_name = f"{category} - {price} KZT"
        text = (
            f"🛍️ *{product_name}*\n\n"
            f"📏 Өлшемдері: {sizes}\n"
            f"🔖 Код: {code}\n\n"
            f"💸 *Бағасы:* {price} KZT\n\n"
            "Тауарды сатып алу үшін нажмите кнопку ниже:"
        )
        bot_username = "smanonline_bot"
        # Ссылка на покупку
        bot_url = f"https://t.me/{bot_username}?start=buy_{code.replace('/', '_')}"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Сатып алу 🛒", url=bot_url))

        # Отправляем сообщение в канал
        if file_id:
            await bot.send_photo(
                chat_id=channel_id,
                photo=file_id,
                caption=text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                chat_id=channel_id,
                text=text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )

        # Уведомляем пользователя об успешной отправке
        await message.reply("Товар успешно отправлен в канал.")
    else:
        await message.reply(f"Товар с кодом {code} не найден.")


from aiogram import types

async def send_product_to_channel(sex: str, price: str):
    # Канал идентификаторы
    channel_id = "@sman_online"

    # Бот сілтемесінің үлгісі
    bot_username = "smanonline_bot"

    # Получаем товары из MongoDB по фильтру
    # Отбираем только "Ерлер" с ценой 37 900
    products = db.getBySexPrice(sex, price)

    for product in products:
        # Извлекаем информацию о товаре
        category = product.get("category", "Ерлер")
        price = product.get("discounted_price", "37 900")
        sizes = ", ".join(map(str, product.get("sizes", [])))
        code = product.get("code", "")
        file_id = product.get("file_id")  # Извлекаем file_id фотографии

        # Подготовка текста сообщения
        product_name = f"{category} - {price} KZT"  # Категория и цена
        text = (
            f"🛍️ *{product_name}*\n\n"
            f"📏 Өлшемдері: {sizes}\n"
            f"🔖 Код: {code}\n\n"
            f"💸 *Бағасы:* {price} KZT\n\n"
            "Тауарды сатып алу үшін төмендегі батырманы басыңыз:"
        )
        
        # Ссылка на покупку с использованием команды /buy
        bot_url = f"https://t.me/{bot_username}?start=buy_{code.replace('/', '_')}"

        # Создание inline-клавиатуры
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("Сатып алу 🛒", url=bot_url))

        # Отправка сообщения в канал с фото или без
        if file_id:
            # Если есть file_id, отправляем фото с описанием
            await bot.send_photo(
                chat_id=channel_id,
                photo=file_id,
                caption=text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            # Если file_id отсутствует, отправляем только текст
            await bot.send_message(
                chat_id=channel_id,
                text=text,
                parse_mode="Markdown",
                reply_markup=keyboard
            )


# Обработчик команды /manager
@dp.message_handler(commands=["manager"])
async def send_managers_info(message: types.Message):
    # Текст для отправки
    managers_text = (
        "@sman_manager_womens - 👤 Әйелдер топтамасының сату менеджері\n\n"
        "@sman_manager_mens - 👤 Ерлер топтамасының сату менеджері"
    )
    # Отправляем сообщение в указанную группу
    channel_id = "@sman_online"
    await bot.send_message(chat_id=channel_id, text=managers_text, parse_mode="Markdown")
    # Подтверждаем пользователю, что сообщение отправлено
    await message.reply("Менеджерлердің ақпараты топқа жіберілді!")



# 🔍 Посмотреть мои заведения
@dp.message_handler(commands=['chats'])
@dp.message_handler(Text(equals="🗣 Менеджермен байланыс"), content_types=['text'])
async def handler(message: types.Message):
    
    await Chat.waiting_for_message.set()

    await message.answer("Напишите сообщение оператору.", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_file_id_and_upload_data(message: types.Message):
    # Получаем file_id
    file_id = message.photo[-1].file_id

    # Получаем текст (подпись к фото)
    if message.caption:
        text = message.caption.strip()
    else:
        await message.reply("Пожалуйста, отправьте фото с подписью.")
        return

    # Разбиваем текст на строки и проверяем формат
    lines = text.strip().split('\n')
    if len(lines) < 3:
        await message.reply("Неправильный формат сообщения. Пожалуйста, отправьте категорию, цену и данные товара.")
        return

    # Извлекаем данные из сообщения
    category = lines[0].strip()
    initial_price = lines[1].strip()
    code_sizes_line = lines[2].strip()

    # Обработка цен
    if initial_price.replace(" ", "") == "57900":
        discounted_price = initial_price
        initial_price = "67 900"
    else:
        discounted_price = initial_price
        initial_price = str(int(initial_price.replace(" ", "")) + 10000)

    # Регулярное выражение для извлечения кода и размеров
    pattern = r'^(?P<code>\w+)/(?P<sizes>[\d,\s]+)$'
    match = re.match(pattern, code_sizes_line)

    if match:
        code = match.group('code')
        sizes_str = match.group('sizes')
        sizes = [int(size.strip()) for size in sizes_str.split(',') if size.strip().isdigit()]

        # Подготовка данных для вставки или обновления
        item_data = {
            'file_id': file_id,
            'category': category,
            'initial_price': initial_price,
            'discounted_price': discounted_price,
            'code': code,
            'sizes': sizes
        }

        # Обновление или добавление в MongoDB
        result = db.upsert_item(code, item_data)

        # Формирование ответа
        sizes_text = ", ".join(map(str, sizes))
        response_text = (
            f"{category} аяқ киімі\n"
            f"🛍️🧔🏻‍♂️{category} аяқ киімі - SALE\n\n"
            f"❌Алғашқы бағасы: {initial_price} тг\n"
            f"✅Жаңа баға: {discounted_price} тг\n\n"
            f"Өлшемдері: {sizes_text}"
        )
        await message.reply(f"Данные успешно {'добавлены' if result != 'Updated' else 'обновлены'}:\n\n{response_text}")
    else:
        await message.reply("Неправильный формат данных. Пожалуйста, используйте формат 'Код/размеры'.")

@dp.message_handler(commands=['get_all'])
async def send_all_items(message: types.Message):
    """Обработчик команды /get_all для отправки всех данных с фотографиями."""
    items = db.get_all_items()
    if not items:
        await message.reply("Нет данных для отображения.")
        return

    for item in items:
        # Извлекаем данные из записи
        file_id = item.get('file_id')
        category = item.get('category', 'Неизвестная категория')
        initial_price = item.get('initial_price', 'Неизвестная цена')
        discounted_price = item.get('discounted_price', 'Неизвестная цена')
        code = item.get('code', 'Неизвестный код')
        sizes = item.get('sizes', [])

        # Формируем текст сообщения с информацией
        sizes_text = ", ".join(map(str, sizes))
        caption = (
            f"{category} аяқ киімі\n"
            f"🛍️🧔🏻‍♂️{category} аяқ киімі - SALE\n\n"
            f"❌Алғашқы бағасы: {initial_price} тг\n"
            f"✅Жаңа баға: {discounted_price} тг\n\n"
            f"Өлшемдері: {sizes_text}"
        )

        # Отправляем фото и текст
        try:
            await bot.send_photo(chat_id=message.chat.id, photo=file_id, caption=caption)
        except Exception as e:
            await message.reply(f"Ошибка при отправке фото для {code}: {str(e)}")



@dp.message_handler(commands=['buy'])
async def buy_command_handler(message: types.Message, state: FSMContext):
    args = message.get_args()  # 'Mp16' сияқты кодты алу

    if args:  # Егер код берілген болса
        product_code = args.strip()  # Кодты алып тастаймыз

        # SHOES_DATA деректерінен тауарды табу
        for category, prices in SHOES_DATA.items():
            for price, products in prices.items():
                for product in products:
                    if product["code"] == product_code:
                        # Forma.s2 күйіне өту және күй деректерін сақтау
                        await state.update_data(type=product_code)
                        await Forma.s2.set()

                        # Пайдаланушыға жауап беру
                        await message.answer(
                            f"Сіз {category} - {price} KZT тауарын таңдадыңыз.\n"
                            f"📏 Өлшемдері: {', '.join(map(str, product['sizes']))}\n"
                            f"🔖 Код: {product_code}\n\n"
                            "Төмендегі батырманы басып таңдауыңызды растаңыз.",
                            reply_markup=btn.cancel() if isinstance(btn.cancel(), InlineKeyboardMarkup) else InlineKeyboardMarkup()
                        )
                        return

        # Егер код табылмаса
        await message.answer("Кешіріңіз, бұл код бойынша тауар табылмады.")
    else:
        await message.answer("Тауар коды дұрыс емес немесе көрсетілмеген.")

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    data = callback_query.data
    message_id = callback_query.message.message_id
    chat_id = callback_query.message.chat.id

    
    # Основное меню
    if data == "buy_shoes_by_code":
        # Показать выбор категории обуви с удалением предыдущего сообщения
        await Forma.s1.set()
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="Тікелей эфирде көрсетілген кодты ✏️ енгізңіз",
            reply_markup=btn.cancel() if isinstance(btn.cancel(), InlineKeyboardMarkup) else InlineKeyboardMarkup()
        )
           
    elif data == "buy_shoes":
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




