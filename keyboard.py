#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import types
import datetime
from load import bot
from database import Database
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Button:
    def __init__(self) -> None:
        pass

    def _create_keyboard(self, btns):

        button = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        for btn in btns:
            button.add(btn)

        return button
    
    def payment(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("💳 Төлем жасау", url="https://pay.kaspi.kz/pay/0wdcrpat"))
        
        return keyboard
    
    def webInsta(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📸 Instagram парақшасы", url="https://www.instagram.com/sman.kz"))
        keyboard.add(types.InlineKeyboardButton("🌐 SMAN веб-сайты", url="https://sman.kz"))
        keyboard.add(InlineKeyboardButton("🔙 Қайту", callback_data="back_to_category"))
        
        return keyboard
    
    def category_selection_keyboard(self):
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("👨 Ерлер аяқ киімі", callback_data="category_men"),
            InlineKeyboardButton("👩 Әйелдер аяқ киімі", callback_data="category_women")
        )
        keyboard.add(InlineKeyboardButton("🔙 Қайту", callback_data="back_to_menu"))
        return keyboard

    def men_shoes_keyboard(self):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("👟 Ерлер кроссовкилары және кедылар", callback_data="men_sneakers"),
            InlineKeyboardButton("🥾 Ерлер бәтеңкелері", callback_data="men_boots"),
            InlineKeyboardButton("👢 Ерлер етігі", callback_data="men_boots_high"),
            InlineKeyboardButton("👞 Ерлер туфлиі", callback_data="men_shoes")
        )
        keyboard.add(InlineKeyboardButton("🔙 Қайту", callback_data="back_to_category"))
        return keyboard

    def women_shoes_keyboard(self):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("👟 Әйелдер кроссовкилары және кедылар", callback_data="women_sneakers"),
            InlineKeyboardButton("🥾 Әйелдер бәтеңкелері", callback_data="women_boots"),
            InlineKeyboardButton("👢 Әйелдер етігі", callback_data="women_boots_high"),
            InlineKeyboardButton("👠 Әйелдер туфлиі", callback_data="women_shoes")
        )
        keyboard.add(InlineKeyboardButton("🔙 Қайту", callback_data="back_to_category"))
        return keyboard






    def buy_cinema(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("🎞 💳 Киноны сатып алу", callback_data="buy_cinema"))
        
        return keyboard
    
    
    def menu(self):
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton("👟 Аяқ киім сатып алу", callback_data="buy_shoes"),
            InlineKeyboardButton("📞 Менеджермен байланысу", callback_data="contact_manager"),
            InlineKeyboardButton("📦 Менің тапсырыстарым", callback_data="my_orders"),
            InlineKeyboardButton("ℹ️ Біз туралы", callback_data="about_us")
        )
        return keyboard

    
    
    def contact_user_button(self, user_id):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("👤 Пайдаланушымен байланысу", callback_data=f"contact_user:{user_id}"))
        return keyboard

    
    def cancel(self):

        k = [
            "⬅️ Выйти из чата"
        ]

        return self._create_keyboard(k)
    
    def admin(self):
        keyboard = [
            "Одобрить заведения",
            "Отклонить заведения",
            "Просмотреть список ожидающих заведений",
        ]

        return self._create_keyboard(keyboard)

    def send_contact(self):

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton("📱 Контактімен бөлісу", request_contact=True))

        return keyboard
