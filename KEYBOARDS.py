from telebot import types
from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def main(k):
    if k == 'no_keyboard':  # 0
        keyboard = types.InlineKeyboardMarkup()

    if k == 'agree':
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Согласен(а) с условиями обмена', callback_data='choose_buy_or_cell'))


    elif k == 'continue':  # 1
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='Продолжить', callback_data='continue'))
        button_support = types.InlineKeyboardButton(text='Поддержка', url='https://t.me/llBANKERll')
        keyboard.add(button_support)

    elif k == 'card_or_qiwi_c':  # 2
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='💳  Карта (скоро появится)', callback_data='comming_soon'))
        keyboard.add(types.InlineKeyboardButton(text='🥝  Киви (комиссия 1%)', callback_data='qiwi_c'))

    elif k == 'card_or_qiwi_b':  # 2
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text='💳  Карта (скоро появится)', callback_data='comming_soon'))
        keyboard.add(types.InlineKeyboardButton(text='🥝  Киви (комиссия 1%)', callback_data='qiwi_b'))

    elif k == 'i_pay_buy':
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="✅Я оплатил", callback_data="check_pay_buy")
        button_2 = types.InlineKeyboardButton(text="⛔️На главную", callback_data="main")
        keyboard.add(button_1, button_2)

    elif k == 'i_pay_cell':
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="✅Я оплатил", callback_data="check_pay_cell")
        button_2 = types.InlineKeyboardButton(text="⛔️На главную", callback_data="main")
        keyboard.add(button_1, button_2)

    elif k == 'choose_buy_or_cell':
        keyboard = types.InlineKeyboardMarkup()
        button_1 = types.InlineKeyboardButton(text="Купить Анд", callback_data="buy")
        button_2 = types.InlineKeyboardButton(text="Продать Анд", callback_data="cell")
        keyboard.add(button_1)
        keyboard.add(button_2)

    return keyboard
