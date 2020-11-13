import time
from selenium import webdriver


def first_open():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x935')
    driver = webdriver.Chrome('databases/chromedriver.exe')
    driver.get('https://antares.trade/personal/');
    time.sleep(1) # Let the user actually see something!
    search_box = driver.find_element_by_name('email')
    search_box.send_keys('banker80@mail.ru') # banker80@mail.ru
    search_box = driver.find_element_by_name('password')
    search_box.send_keys('jezqaq-zUssom-gapwe7') # jezqaq-zUssom-gapwe7
    search_box = driver.find_element_by_class_name('button')
    search_box.click()
    search_box = driver.find_element_by_class_name('main_personal_name')
    search_box.click()
    return driver


def check_balance():
    while True:
        try:
            driver = first_open()
            elems = driver.find_elements_by_class_name('bill_amount')
            start_account = elems[0].text
            bonus_account = elems[1].text
            operation_account = elems[2].text
            driver.close()
            return {'start_balance': start_account, 'bonus_balance': bonus_account, 'operation_balance': operation_account}
        except Exception:
            time.sleep(3)


def make_transfer(driver, id, transfer_amount, message):
    driver.get('https://antares.trade/personal/binar/transfers/')
    search_box = driver.find_element_by_name('transfers_id')
    search_box.send_keys(id)
    search_box = driver.find_element_by_name('transfers_amount')
    search_box.send_keys(transfer_amount)
    search_box = driver.find_element_by_name('transfers_message')
    search_box.send_keys(message)
    time.sleep(4)
    search_box = driver.find_elements_by_tag_name('input')[-1]
    search_box.click()
    time.sleep(0.1)  #
    search_box = driver.find_element_by_class_name('checkbox')  #
    search_box.click()
    time.sleep(0.1)
    search_box = driver.find_element_by_class_name('transfers2')
    search_box.click()


def check_operation(message, money):
    while True:
        #try:
        if True:
            driver = first_open()
            driver.get('https://antares.trade/personal/binar/history/')
            search_box = driver.find_element_by_class_name('form_btn').find_element_by_tag_name('input')
            time.sleep(3)
            search_box.click()
            search_box = driver.find_elements_by_class_name('big_history_table_tbody_tr')
            sp = []
            idx = 0
            word = ''
            for i in search_box:
                dd = (i.find_elements_by_tag_name('div'))
                for d in dd:
                    idx += 1
                    if idx == 2:
                        word = d.text.split()[-1]
                    if idx == 3:
                        print(word, message, [d.text])
                        idx = 0
                        d = d.text.split()
                        if word.upper() == message.upper():
                            if '+' in d[0]:
                                if float(money) >= float(str(d[1])):
                                    driver.close()
                                    return '1'
                        word = ''
            driver.close()
            return '0'
        #except Exception:
        #    pass


def main(id, sum):
    driver = first_open()
    make_transfer(driver, id, sum, 'Перевод от Antares бота. Хорошего дня.')
    driver.close()



