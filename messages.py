import bs4
import requests

import antares
import qiwi
from databases import db_connrect


def usd():
    while True:
        try:
            url = 'https://www.banki.ru/products/currency/cb/'
            r = requests.get(url)
            b = bs4.BeautifulSoup(r.text, features='lxml')
            b = b.find_all({'td': {'data-test': "currency-table-row"}})
            return float(str(b[3]).replace('<td>', '').replace('</td>', ''))
        except Exception:
            pass


def from_button(message, data):
    stage = db_connrect.get_user_info_bd(message.chat.id)[1]['stage']
    target = db_connrect.get_user_info_bd(message.chat.id)[1]['target']
    bank = db_connrect.get_user_info_bd(message.chat.id)[1]['bank']
    if data == '':
        if stage == 1:
            data = 'choose_buy_or_cell'
        if stage == 2:
            data = target
        if stage == 3:
            if target == 'buy':
                data = 'qiwi_b'
            if target == 'cell':
                data = 'qiwi_c'

    answer, keyboard = '', 'no_keyboard'

    if data == 'choose_buy_or_cell' or data == 'main' or data == 'continue':  # 1
        if data == 'main':
            db_connrect.update_bd(0, 'stage', message.chat.id)
            db_connrect.update_bd('', 'target', message.chat.id)
            db_connrect.update_bd('', 'bank', message.chat.id)
            db_connrect.update_bd(0, 'count', message.chat.id)
            db_connrect.update_bd(0, 'max_sum', message.chat.id)
            db_connrect.update_bd('', 'keyword', message.chat.id)
        answer = 'Выберите операцию для продолжения'
        keyboard = 'choose_buy_or_cell'
        db_connrect.update_bd(1, 'stage', message.chat.id)
    elif data == 'buy':
        answer = 'Вы выбрали: купить AND\nВарианты пополения:'
        keyboard = 'card_or_qiwi_b'
        db_connrect.update_bd('buy', 'target', message.chat.id)
        db_connrect.update_bd(2, 'stage', message.chat.id)
    elif data == 'cell':
        answer = 'Вы выбрали: продать AND\nВарианты пополения:'
        keyboard = 'card_or_qiwi_c'
        db_connrect.update_bd(2, 'stage', message.chat.id)
        db_connrect.update_bd('cell', 'target', message.chat.id)
    elif data == 'qiwi_b':
        balance = antares.check_balance()['operation_balance']
        db_connrect.update_bd(3, 'stage', message.chat.id)
        db_connrect.update_bd('buy', 'target', message.chat.id)
        db_connrect.update_bd('qiwi', 'bank', message.chat.id)
        db_connrect.update_bd(int(float(balance)), 'max_sum', message.chat.id)
        if float(balance) < 5:
            answer = 'Сервис временно недоступен.\nПожалуйста, повторите попытку позднее.'
            keyboard = 'no_keyboard'
        else:
            answer = f'Выбраный способ оплаты: Киви кошелек\nВведите желаемую к обмену сумму от 5 до {int(float(balance))} (валюта AND)'
            keyboard = 'no_keyboard'

    elif data == 'qiwi_c':
        balance = antares.check_balance()['operation_balance']
        db_connrect.update_bd(int(float(balance)), 'max_sum', message.chat.id)
        db_connrect.update_bd(3, 'stage', message.chat.id)
        db_connrect.update_bd('cell', 'target', message.chat.id)
        db_connrect.update_bd('qiwi', 'bank', message.chat.id)
        if False:
            pass
        else:
            answer = f'Выбраный способ вывода: Киви кошелек\nВведите желаемую к обмену сумму от 5 AND'
            keyboard = 'no_keyboard'
    elif data == 'check_pay_buy':
        info = db_connrect.get_user_info_bd(message.chat.id)[1]
        if info['bank'] == 'qiwi':
            while True:
                result, addr = qiwi.check_transaction('79521940783', '7e013ca9c29f9cef2761b25679b7c6d4',
                                                      info['keyword'], info['money'])
                if result != '9':
                    break
            if result == '0':
                if not 'Оплата не поступила! Попробуйте снова.' in message.text:
                    answer = f'Оплата не поступила! Попробуйте снова.\n\n{message.text}'
                    keyboard = 'i_pay_buy'
                else:
                    answer = message.text
                    keyboard = 'i_pay_buy'
            if result == '1':
                if info['keyword'] != '':
                    db_connrect.update_bd('', 'keyword', message.chat.id)
                    antares.main(addr, str(int(float(info['money']) // usd())))  # check
                    answer = 'Перевод выполнен успешно.'
                    keyboard = 'continue'
                else:
                    answer = 'Выплата уже была произведена.'
                    keyboard = 'continue'
    elif data == 'check_pay_cell':
        info = db_connrect.get_user_info_bd(message.chat.id)[1]
        if info['bank'] == 'qiwi':
            result = antares.check_operation(info['keyword'], info['money'])
            if result == '1':
                answer = 'Перевод найден! Введите номер киви для отправления средств'
                keyboard = 'no_keyboard'
                db_connrect.update_bd(99, 'stage', message.chat.id)
            else:
                answer = 'Перевод не найден!'
                keyboard = 'i_pay_cell'
    return answer, keyboard


def from_message(user_answer):
    answer, keyboard = '', 'no_keyboard'
    text_answer = user_answer.text.strip().upper()

    if text_answer == '/START' or text_answer == 'START' or text_answer == 'СТАРТ':
        db_connrect.update_bd(0, 'stage', user_answer.chat.id)
        db_connrect.update_bd('', 'target', user_answer.chat.id)
        db_connrect.update_bd('', 'bank', user_answer.chat.id)
        db_connrect.update_bd(0, 'count', user_answer.chat.id)
        db_connrect.update_bd(0, 'max_sum', user_answer.chat.id)
        db_connrect.update_bd('', 'keyword', user_answer.chat.id)
        db_connrect.update_bd(0, 'money', user_answer.chat.id)
        answer = f'Я - бот обменник. Для обмена использую:\n\n' \
                 f'- Систему Быстрых Платежей\n(https://sbp.nspk.ru/participants/)\n\n- Qiwi\n\nКомиссия за обмен - 1%\n\n' \
                 f'Если условия обмена вас устраивают и вы желаете продолжить, тогда нажмите на кнопку ' \
                 f'«Согласен(а) с условиями обмена»'
        keyboard = 'agree'
    info = db_connrect.get_user_info_bd(user_answer.chat.id)[1]
    print(info)
    if info['stage'] == 99:
        qiwi.send_p2p('', user_answer.text, 'Перевод от бота Antares. Хорошего дня.', info['money'])
        answer = 'Перевод выполнен.'
        keyboard = 'continue'

    elif text_answer.isdigit() and info['stage'] == 3:
        if not 5 <= int(text_answer) <= int(info['max_sum']) and info['target'] == 'buy':
            answer = f'Введите верные данные!\nВведите желаемую к обмену сумму от 5 до {info["max_sum"]} (валюта AND)'
            keyboard = 'no_keyboard'
        else:
            db_connrect.update_bd(int(text_answer), 'count', user_answer.chat.id)
            db_connrect.update_bd(4, 'stage', user_answer.chat.id)
            if info['target'] == 'buy':
                answer = 'Введите номер кошелька который нужно пополнить'
            if info['target'] == 'cell':
                answer = 'Введите номер кошелька с которого будет сделан перевод'
            keyboard = 'no_keyboard'

    elif info['stage'] == 4:
        usd_1 = usd()
        key = db_connrect.generate_keyword() + '_' + text_answer
        db_connrect.update_bd(key, 'keyword', user_answer.chat.id)
        db_connrect.update_bd(5, 'stage', user_answer.chat.id)
        db_connrect.update_bd(float(info['count']) * round(usd_1, 2) * 1.01, 'money', user_answer.chat.id)
        if info['target'] == 'buy':
            money = float(info['count']) * round(usd_1, 2) * 1.01
            if info['bank'] == 'qiwi':
                n_k = '+79222662956'
                answer = f'Комментарий находится в сообщении ВЫШЕ!\nВыбранное действие: покупка {info["count"]} AND за {round(money, 0)} RUB ' \
                         f'(курс ЦБ {str(round(usd_1, 0))}).\nДля перевода средств скопируйте комментарий к' \
                         f' платежу и переведите средства по номеру \n{n_k} в Qiwi. Ссылка для перевода:' \
                         f' https://qiwi.com/payment/form/99\n\nВНИМАНИЕ!\nКомментарий к платежу' \
                         f' обязателен!\n\n\nНажмите кнопку «✅ Я оплатил» ПОСЛЕ отправки денежных средств, ' \
                         f'в противном случае нажмите кнопку «⛔️На главную».'
                keyboard = 'i_pay_buy'

        if info['target'] == 'cell':
            if info['bank'] == 'qiwi':
                account_money_and = 'RU013742216'
                money = float(info['count']) * round(usd_1, 2) * 1.01
                answer = f'Комментарий находится в сообщении ВЫШЕ!\nЧтобы получить {round(money, 0)} RUB за {info["count"]} AND на' \
                         f' счет {account_money_and}\n\nВНИМАНИЕ!\nКомментарий к платежу обязателен!\nНажмите кнопку' \
                         f' «✅ Я оплатил» ПОСЛЕ отправки средств, в противном случае нажмите кнопку «⛔️На главную».',
                keyboard = 'i_pay_cell'


    return answer, keyboard
