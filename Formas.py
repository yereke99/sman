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
from config import admin, admin3
from datetime import datetime
from traits import *
import time
from traits import*
from config import*
import os
from aiogram.types import InputMediaPhoto, InputMediaVideo
from data import SHOES_DATA
from mongo import*



db = MongoDB()
btn = Button()



# Ensure the directory exists
os.makedirs('./pdf/', exist_ok=True)

class Forma(StatesGroup):
    s1 = State()  
    s2 = State()
    s3 = State() 
    s4 = State()
    s5 = State()
    s6 = State()
    s7 = State()


# Функция тауарды және оның өлшемін сөздіктен алып тастау үшін
def remove_item_from_inventory(code, size):
    for category, prices in SHOES_DATA.items():
        for price, products in prices.items():
            for product in products:
                if product["code"].lower() == code.lower():
                    if size in product["sizes"]:
                        product["sizes"].remove(size)
                        # Егер өлшемдер тізімі бос болса, тауарды алып тастау
                        if not product["sizes"]:
                            products.remove(product)
                        return True
    return False


# Бағаны табу функциясы
def get_price_by_code(code):
    for category, prices in SHOES_DATA.items():
        for price, products in prices.items():
            for product in products:
                if product["code"].lower() == code.lower():
                    return price
    return None

# Функция, код бойынша бағаны табу үшін
def get_price_by_code_and_size(code, size):
    for category, prices in SHOES_DATA.items():
        for price, products in prices.items():
            for product in products:
                if product["code"].lower() == code.lower() and size in product["sizes"]:
                    return price
    return None

def get_sizes_by_code(code):
    for category, prices in SHOES_DATA.items():
        for price, products in prices.items():
            for product in products:
                if product["code"].lower() == code.lower():
                    return product["sizes"]
    return None

def find_product_by_code(code):
    for category, prices in SHOES_DATA.items():
        for price, products in prices.items():
            for product in products:
                if product["code"].lower() == code.lower():
                    return price, product["sizes"]
    return None, None


@dp.message_handler(state='*', commands='🔕 Сатып алуды тоқтату')
@dp.message_handler(Text(equals='🔕 Сатып алуды тоқтату', ignore_case=True), state='*')
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
    
    # Завершение состояния и отправка сообщения без кнопок
    await state.finish()
    await message.reply('Сіз тапсырыстан бас тарттыңыз.', reply_markup=types.ReplyKeyboardRemove())
    
    # Отправка меню после удаления кнопок
    await message.reply("Таңдаңыз:", reply_markup=btn.menu())


@dp.message_handler(state=Forma.s1)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text.strip()

    price, sizes = find_product_by_code(data['type'])
    
    if price and sizes:
        await Forma.next()
        await message.reply(f"Бағасы: {price} KZT\nҚол жетімді өлшемдер: {', '.join(map(str, sizes))}", reply_markup=btn.buy())
       
    else:
        await message.reply("Бұл кодпен тауар табылмады. @smanonline_bot каналдан басқа аяқ киімдер көріңіз!", reply_markup=btn.menu())
        await state.finish()



# Күй Forma.s2 үшін өңдеуші функция
@dp.message_handler(state=Forma.s2)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data['type']
        available_sizes = get_sizes_by_code(code)

    if available_sizes:
        await Forma.next()

        # Батырмалармен бірге өлшемдер тізімін жіберу
        await message.reply("Қол жетімді өлшемдерді таңдаңыз:", reply_markup=btn.size_keyboard(available_sizes))
        
    else:
        await message.reply("Бұл кодпен тауар табылмады. @smanonline_bot каналдан басқа аяқ киімдер көріңіз!", reply_markup=btn.menu())
        await state.finish()



# Күй Forma.s3 үшін өңдеуші функция
@dp.message_handler(state=Forma.s3)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data.get('type')
        try:
            size = int(message.text)
            data['size'] = size
        except ValueError:
            await message.reply("Өлшемді сан түрінде енгізіңіз.")
            return
    
    # Бағаны табу с использованием метода MongoDB
    price = db.get_price_by_code_and_size(code, size)
    
    if price:
        await Forma.next()
        await message.reply(f"Бағасы: {price} KZT. Тапсырыс бересіз бе?", reply_markup=btn.approve())
    else:
        await message.reply("Өкінішке орай, бұл өлшемде тауар жоқ, басқа өлшемдегі аяқ киімдерді көріңіз.", reply_markup=btn.menu())
        await state.finish()


@dp.message_handler(state=Forma.s4)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data.get('type')
        size = data.get('size')
        data['approve'] = message.text
        data['price'] = db.get_price_by_code(code)  # Используем метод для извлечения цены

    # Если пользователь выбрал "✔️ Иә" для подтверждения заказа
    if data['approve'] == "✔️ Иә":
        price = data['price']
        
        if price:
            await Forma.next()  # Переход к следующему состоянию
            with open("/home/sman/photo/example.jpeg", 'rb') as photo:
                await bot.send_photo(
                    message.from_user.id,
                    photo=photo,
                    caption=f"Төлеуге қажет сома: {price} KZT.\nСілтеме арқылы төлем жасаңыз және pdf чекті Поделится деген түймені баса отыра телеграмм ботқа кері жіберіңіз",
                    reply_markup=btn.payment(),
                )
        else:
            # Если цена не найдена для данного кода
            await message.reply("Кешіріңіз, бұл кодпен баға табылмады.", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()

    # Если пользователь не выбрал "✔️ Иә"
    else:
        await message.reply("Тапсырыс аяқталды.", reply_markup=btn.menu())
        await state.finish()



@dp.message_handler(lambda message: not (message.document and message.document.mime_type == 'application/pdf'), state=Forma.s2, content_types=types.ContentType.DOCUMENT)
async def pdf_validator(message: types.Message, state: FSMContext):
    await message.reply(".pdf файл форматымен жіберіңіз!")
    await Forma.s4.set()

@dp.message_handler(state=Forma.s5, content_types=types.ContentType.DOCUMENT)
async def handler(message: types.Message, state: FSMContext):
    try:
        document = message.document

        # Генерация уникального имени файла
        user_id = message.from_user.id
        timestamp = int(time.time())
        random_int = Generator.generate_random_int()
        file_name = f"{user_id}_{timestamp}_{random_int}.pdf"
        file_path = os.path.join('./pdf/', file_name)

        # Загрузка PDF-файла
        file_info = await bot.get_file(document.file_id)
        await bot.download_file(file_info.file_path, file_path)

        # Обработка PDF-файла
        pdf_reader = PDFReader(file_path)
        pdf_reader.open_pdf()
        result = pdf_reader.extract_specific_info()
        pdf_reader.close_pdf()

        async with state.proxy() as data:
            data['data'] = message.text
            data['pdf_result'] = result
            data['fileName'] = file_name

        expected_price = convert_currency_to_int(data['price'])
        actual_price = convert_currency_to_int(data['pdf_result'][2])

        # Проверка корректности суммы
        if actual_price != expected_price:
            await bot.send_message(
                message.from_user.id,
                text="*Төленетін сумма қате!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu()
            )
            # Уведомление администраторов о несоответствии суммы
            for admin_id in [admin, admin2, admin3, admin4]:
                await bot.send_document(
                    admin_id,
                    document=document.file_id,
                    caption=(
                        f"❌ Қате төлем.\n\n"
                        f"🔖 Тауар коды: {data['type']}\n"
                        f"📏 Өлшем: {data['size']}\n"
                        f"💰 Күтілетін сома: {expected_price} KZT\n"
                        f"💸 Төленген сома: {actual_price} KZT\n\n"
                        "Құжатта қате сома көрсетілген."
                    ),
                    reply_markup=types.ReplyKeyboardRemove(),
                )
            await state.finish()
            return

        # Проверка продавца
        if data['pdf_result'][4] not in ["Сатушының ЖСН/БСН 190540002794", "ИИН/БИН продавца 190540002794"]:
            await bot.send_message(
                message.from_user.id,
                text="*Дұрыс емес счетқа төледіңіз!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu()
            )
            # Уведомление администраторов о неверном продавце
            for admin_id in [admin, admin2, admin3, admin4]:
                await bot.send_document(
                    admin_id,
                    document=document.file_id,
                    caption=(
                        f"❌ Қате төлем.\n\n"
                        f"🔖 Тауар коды: {data['type']}\n"
                        f"📏 Өлшем: {data['size']}\n"
                        f"💰 Сома: {expected_price} KZT\n\n"
                        "Құжаттағы сатушының деректері дұрыс емес."
                    ),
                    reply_markup=types.ReplyKeyboardRemove()
                )
            await state.finish()
            return

        # Удаление размера из инвентаря после подтверждения оплаты
        if db.remove_item_from_inventory(data['type'], data['size']):
            await Forma.next()
            await bot.send_message(
                message.from_user.id,
                text="*Сізбен кері 📲 байланысқа шығу үшін байланыс нөміріңізді қалдырыңыз! Төменде тұрған \n\n📱 Контактімен бөлісу кнопкасын басыныз\n\nЕШҚАШАН САНДАРМЕН ЖАЗБАЙМЫЗ ‼️*",
                parse_mode="Markdown",
                reply_markup=btn.send_contact()
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text="*Сатып алынған тауарды сөздіктен алып тастау сәтсіз аяқталды, менеджерге хабарласаңыз.*",
                parse_mode="Markdown",
                reply_markup=types.ReplyKeyboardRemove(),
                
            )
            await state.finish()

    except Exception as e:
        print(e)
        for admin_id in [admin, admin2, admin3, admin4]:
            await bot.send_message(
                admin_id,
                text=f"Error: {str(e)}",
            )
        await Forma.s2.set()
        await bot.send_message(
            message.from_user.id,
            text="Төлем жасаған соң чекті 📲 .pdf форматында жіберіңіз!\n\n*НАЗАР АУДАРЫҢЫЗ ЧЕКТІ МОДЕРАТОР ТЕКСЕРЕДІ\n\n ЕСКЕРТУ ❗️\nЖАЛҒАН ЧЕК ЖІБЕРУ НЕМЕСЕ БАСҚАДА ДҰРЫС ЕМЕС ЧЕКТЕР ЖІБЕРУ АВТОМАТТЫ ТҮРДЕ САТЫП АЛУДЫҢ КҮШІН ЖОЯДЫ*",
            parse_mode="Markdown",
            reply_markup=btn.cancels()
        )


@dp.message_handler(state=Forma.s6, content_types=types.ContentType.CONTACT)
async def handler(message: types.Message, state: FSMContext):
    await Forma.next()

    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number

    # Қолданушыға жылы әрі достық хабарлама жіберу
    await message.reply(
        "Мекен-жайыңызды ✏️ енгізіңіз",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(state=Forma.s7)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
        contact = data.get('contact')
        code = data.get('type')
        size = data.get('size')
        price = data.get('price')
        file_name = data.get('fileName')
        file_path = os.path.join('./pdf/', file_name)

    # Отправка сообщения пользователю
    await message.reply(
        f"🎉 *Сатып алғаныңыз үшін рақмет!* 🎉\n\n"
        f"Сіз {code} кодымен, {size} өлшемдегі тауарды {price} KZT-ға сатып алдыңыз.\n"
        f"📄 Төлем расталды. Сіздің чегіңіз: {file_name}\n\n"
        f"👨‍💼 *Менеджер сізбен жақын арада байланысады.*\n"
        f"📞 Қосымша сұрақтар бойынша бізге хабарласа аласыз!\n\n"
        f"Сізге жағымды күн және сәттілік тілейміз! 😊",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )

    # Отправка уведомления администраторам с PDF-файлом
    for admin_id in [admin, admin2, admin3, admin4]:
        try:
            await bot.send_document(
                admin_id,
                document=open(file_path, 'rb'),
                caption=(
                    f"✅ *Жаңа тапсырыс төленді!*\n\n"
                    f"🔖 Тауар коды: {code}\n"
                    f"📏 Өлшем: {size}\n"
                    f"💸 Төлем сомасы: {price} KZT\n"
                    f"📞 Байланыс нөмірі: {contact}\n"
                    f"📍 Мекенжай: {data['address']}\n\n"
                    "Тапсырыс сәтті қабылданды, оны өңдеуге дайын болыңыз."
                ),
                parse_mode="Markdown"
            )
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение администратору {admin_id}: {e}")

    await state.finish()
