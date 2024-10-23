#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aiogram import types
import datetime
from load import bot
from database import Database

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
    
    def buy_cinema(self):

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("🎞 💳 Киноны сатып алу", callback_data="buy_cinema"))
        
        return keyboard
    
    
    def menu(self):
        keyboard = [
            "Добавить заведение",
            "Посмотреть мои заведения",
            "Проверить баллы и скидочную карту",
            "Профиль",
        ]

        return self._create_keyboard(keyboard)
    
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
