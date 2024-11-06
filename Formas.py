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
from aiogram.types import InputMediaPhoto, InputMediaVideo
from data import SHOES_DATA



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


@dp.message_handler(state=Forma.s1)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text.strip()

    price, sizes = find_product_by_code(data['type'])
    
    if price and sizes:
        await Forma.next()
        await message.reply(f"Бағасы: {price} KZT\nҚол жетімді өлшемдер: {', '.join(map(str, sizes))}", reply_markup=btn.buy())
       
    else:
        await message.reply("Бұл кодпен тауар табылмады.", reply_markup=btn.menu())
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
        await message.reply("Бұл кодпен тауар табылмады.", reply_markup=btn.menu())
        await state.finish()



# Күй Forma.s3 үшін өңдеуші функция
@dp.message_handler(state=Forma.s3)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data.get('type')
        size = int(message.text)
        data['size'] = size
    
    # Бағаны табу
    price = get_price_by_code_and_size(code, size)
    
    if price:
        await Forma.next()
        await message.reply(f"Бағасы: {price} KZT. Тапсырыс бересіз бе?", reply_markup=btn.approve())
    else:
        await message.reply("Өкінішке орай, бұл өлшемде тауар жоқ, басқа өлшемдегі аяқ киімдерді көріңіз көріңі.", reply_markup=btn.menu())
        await state.finish()


@dp.message_handler(state=Forma.s4)
async def handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        code = data.get('type')
        size = data.get('size')
        data['approve'] = message.text
        data['price'] = get_price_by_code(code)

    # Қолданушы "Иә" деп таңдаса
    if data['approve'] == "✔️ Иә":
        price = get_price_by_code(code)
        
        if price:
            await Forma.next()  # Келесі күйге өту
            await message.reply(
                f"Төлеуге қажет сома: {price} KZT.\nСілтеме арқылы төлем жасаңыз және pdf чекті Поделится деген түймені баса отыра телеграмм ботқа кері жіберіңіз",
                reply_markup=btn.payment(),
            )

        else:
            await message.reply("Кешіріңіз, бұл кодпен баға табылмады.")
            await state.finish()

    # Егер қолданушы "Иә" деп жауап бермесе
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

        # Уникалды файл атауын генерациялау
        user_id = message.from_user.id
        timestamp = int(time.time())
        random_int = Generator.generate_random_int()
        file_name = f"{user_id}_{timestamp}_{random_int}.pdf"
        file_path = os.path.join('./pdf/', file_name)

        # PDF файлды жүктеу
        file_info = await bot.get_file(document.file_id)
        await bot.download_file(file_info.file_path, file_path)

        # PDF файлды өңдеу
        pdf_reader = PDFReader(file_path)
        pdf_reader.open_pdf()
        result = pdf_reader.extract_specific_info()
        pdf_reader.close_pdf()

        async with state.proxy() as data:
            data['data'] = message.text
            data['pdf_result'] = result
            data['fileName'] = file_name

        print(data['pdf_result'][2])
        print(data['price'])  # Бағаны басып шығару
        
        if convert_currency_to_int(data['pdf_result'][2]) != convert_currency_to_int(data['price']): 
            await bot.send_message(
                message.from_user.id,
                text="*Төленетін сумма қате!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu()
            )  
            await state.finish() 
            return
        
        print(data['pdf_result'][4])

        if data['pdf_result'][4] == "Сатушының ЖСН/БСН 190540002794" or data['pdf_result'][4] == "ИИН/БИН продавца 190540002794":
        
            """
            # Егер чек бұған дейін төленген болса
            if db.CheckLoto(data['pdf_result'][3]) == True:
                await bot.send_message(
                    message.from_user.id,
                    text="*ЧЕК ТӨЛЕНІП ҚОЙЫЛҒАН!\nҚайталап көріңіз*",
                    parse_mode="Markdown",
                    reply_markup=btn.menu_not_paid()
                )  
                await state.finish() 
                return
            """
            
            # Төлем расталғаннан кейін тауар мен өлшемді алып тастау
            if remove_item_from_inventory(data['type'], data['size']):
                await Forma.next()
                await bot.send_message(
                    message.from_user.id,
                    text="*Сізбен кері 📲 байланысқа шығу үшін байланыс нөміріңізді қалдырыңыз! Төменде тұрған \n\n📱 Контактімен бөлісу кнопкасын басыныз\n\nЕШҚАШАН САНДАРМЕН ЖАЗБАЙМЫЗ ‼️*",
                    parse_mode="Markdown",
                    reply_markup=btn.send_contact()
                )
                return
            else:
                await bot.send_message(
                    message.from_user.id,
                    text="*Сатып алынған тауарды сөздіктен алып тастау сәтсіз аяқталды, менеджерге хабарласаңыз.*",
                    parse_mode="Markdown"
                )
                await state.finish()
                return
        
        await bot.send_message(
                message.from_user.id,
                text="*Дұрыс емес счетқа төледіңіз!\nҚайталап көріңіз*",
                parse_mode="Markdown",
                reply_markup=btn.menu()
            )  
        await state.finish() 

    except Exception as e:
        print(e)
        await bot.send_message(
            admin,
            text="Error: %s"%str(e),
        ) 
        await Forma.s2.set()
        await bot.send_message(
                message.from_user.id,
                text="Төлем жасаған соң чекті 📲 .pdf форматында жіберіңіз!\n\n*НАЗАР АУДАРЫҢЫЗ ЧЕКТІ МОДЕРАТОР ТЕКСЕРЕДІ\n\n ЕСКЕРТУ ❗️\nЖАЛҒАН ЧЕК ЖІБЕРУ НЕМЕСЕ БАСҚАДА ДҰЫРЫС ЕМЕС ЧЕКТЕР ЖІБЕРУ АВТОМАТТЫ ТҮРДЕ САТЫП АЛУДЫҢ КҮШІН ЖОЯДЫ*",
                parse_mode="Markdown",
                reply_markup=btn.cancel()
            ) 


@dp.message_handler(state=Forma.s6, content_types=types.ContentType.CONTACT)
async def handler(message: types.Message, state: FSMContext):
    await Forma.next()

    async with state.proxy() as data:
        data['contact'] = message.contact.phone_number

    # Қолданушыға жылы әрі достық хабарлама жіберу
    await message.reply(
        "Мекен-жайыңызды ✏️ енгізіңіз",
        parse_mode="Markdown"
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

    # Қолданушыға жылы әрі достық хабарлама жіберу
    await message.reply(
        f"🎉 *Сатып алғаныңыз үшін рақмет!* 🎉\n\n"
        f"Сіз {code} кодымен, {size} өлшемдегі тауарды {price} KZT-ға сатып алдыңыз.\n"
        f"📄 Төлем расталды. Сіздің чегіңіз: {file_name}\n\n"
        f"👨‍💼 *Менеджер сізбен жақын арада байланысады.*\n"
        f"📞 Қосымша сұрақтар бойынша бізге хабарласа аласыз!\n\n"
        f"Сізге жағымды күн және сәттілік тілейміз! 😊",
        parse_mode="Markdown"
    )

    await state.finish()

