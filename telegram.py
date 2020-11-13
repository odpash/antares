import ast
import random
import time
from databases import db_connrect
import requests
import telebot
import qiwi, antares
import bs4
from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import KEYBOARDS
import messages
TOKEN_HTTP_API = '1405134894:AAF6VlsfOOGgVzahAzhAN9JLuKR6uiLYO6U'
bot = telebot.TeleBot(TOKEN_HTTP_API)



def send_text_message(text, about, k):
    info = list(db_connrect.get_user_info_bd(about.chat.id))[1]
    stages = [f'Добро пожаловать, {about.chat.first_name}!', 'Здесь вы можете приобрести/продать AND.\n'
            'Минимальная сумма операции 5 монет.', 'Выберите удобный для Вас вариант пополнения / вывода средств',
              'Раздел: сумма перевода', 'Пример: RU1234567890', info['keyword']]
    print(text)
    try:
        try:
            word = stages[info['stage']]
            if 3 > info['stage'] > 1:
                button_back = KeyboardButton('Назад')
                button_support = KeyboardButton('Поддержка')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                greet_kb.add(button_back, button_support)
                bot.send_message(about.chat.id, word, reply_markup=greet_kb)
            else:
                button_back = KeyboardButton('На главную')
                greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
                greet_kb.add(button_back)
                bot.send_message(about.chat.id, word, reply_markup=greet_kb)
        except Exception:
            pass
        bot.send_message(about.chat.id, text, reply_markup=KEYBOARDS.main(k))
        for i in range(50):
            try:
                bot.delete_message(about.chat.id, str(int(about.message_id) - i))
            except Exception:
                pass

    except Exception:
        pass
    print(db_connrect.get_user_info_bd(about.chat.id)[1])
        # bot.answer_callback_query(call.id, text="Дата выбрана")
    #except Exception:
    #    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        message, keyboard = messages.from_button(call.message, call.data)
        print(message, keyboard)
        send_text_message(message, call.message, keyboard)


@bot.message_handler(content_types=["text"])
def get_user_answer(user_answer):
    message, keyboard = messages.from_message(user_answer)
    if user_answer.text == 'На главную':
        db_connrect.update_bd(1, 'stage', user_answer.chat.id)
        message, keyboard = messages.from_button(user_answer, '')
        send_text_message(message, user_answer, keyboard)
    elif user_answer.text.strip().upper() == 'ПОДДЕРЖКА':
        button_back = KeyboardButton('Вернуться к боту')
        greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        greet_kb.add(button_back)
        bot.send_message(user_answer.chat.id, 'Для получения поддержки обратитесь к администратору.\n'
                                              'Ссылка: https://t.me/llBANKERll', reply_markup=greet_kb)
    elif user_answer.text == 'Вернуться к боту':
        message, keyboard = messages.from_button(user_answer, '')
        send_text_message(message, user_answer, keyboard)

    elif user_answer.text == 'Назад':
        info = db_connrect.get_user_info_bd(user_answer.chat.id)[1]['stage'] - 1
        print(info)
        if info < 1:
            info = 1
        db_connrect.update_bd(info, 'stage', user_answer.chat.id)
        message, keyboard = messages.from_button(user_answer, '')
        send_text_message(message, user_answer, keyboard)
    elif message != '':
        send_text_message(message, user_answer, keyboard)


bot.polling()
 