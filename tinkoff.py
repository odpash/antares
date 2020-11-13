import ast
import random
import time
from selenium import webdriver


def first_open():
    driver = webdriver.Chrome('databases/chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get('https://www.tinkoff.ru/login/');
    time.sleep(1) # Let the user actually see something!
    search_box = driver.find_element_by_name('login')
    search_box.send_keys('89222662956') # banker80@mail.ru
    search_box = driver.find_element_by_class_name('pw5ce')
    search_box.click()
    time.sleep(30)
    search_box = driver.find_element_by_name('password')
    search_box.send_keys('Ghbjhbntn1')#G
    search_box = driver.find_element_by_class_name('pw5ce')
    search_box.click()
    time.sleep(3)
    return driver


def check(driver):
    with open('cards.txt', 'r', encoding='UTF-8') as f:
        a = f.read().split('\n')
    with open('cards.txt', 'w', encoding='UTF-8') as f:
        f.write('')
    sp = []
    for i in range(len(a)):
        try:
            sp.append(ast.literal_eval(a[i]))
        except Exception:
            pass
    final_sp = []
    if len(sp) == 0:
        return False, ''
    for elem in sp:
        if elem['is_used'] == False:
            final_sp.append(elem)
    return True, final_sp


def check_operation(driver, sp):
    keywords = []
    for i in sp:
        keywords.append(i['secret_message'])
    driver.get('https://www.tinkoff.ru/events/feed/?preset=all&pieType=Debit')
    time.sleep(10)
    search_box = driver.find_element_by_class_name('Button__buttonWrapper_size_m_2uIME')
    search_box.click()
    time.sleep(0.2)
    search_box.click()
    time.sleep(0.2)
    search_box.click()
    time.sleep(0.2)
    search_box.click()
    time.sleep(0.2)
    search_box.click()
    time.sleep(0.2)
    search_box.click()
    time.sleep(0.2)
    data = driver.find_element_by_class_name('TimelineList__list_2pdmA').text.split('Tinkoff Black')
    answers = []
    for keyword in keywords:
        fl = False
        for d in data:
            d = d.split('\n')
            for i in d:
                print(i, keyword)
                if keyword.lower() in i.lower():
                    kk = i.split('_')
                    answers.append({'keyword': kk[0], 'addr': kk[1], 'money': float(d[1].replace('+', '').replace(',', '.'))})
                    fl = True
                    break
            if fl:
                break
    print(answers)
    with open('cards_result.txt', 'a', encoding='UTF-8') as f:
        for i in answers:
            f.write('\n')
            f.write(str(i))
        f.close()

def wait(driver):
    x = 0
    link_now = 'https://www.tinkoff.ru/summary/?auth=null&large=null'
    links = ['https://www.tinkoff.ru/summary/?auth=null&large=null', 'https://www.tinkoff.ru/events/feed/?auth=null&large=null', 'https://www.tinkoff.ru/payments/', 'https://www.tinkoff.ru/bonuses/?auth=null&large=null', 'https://www.tinkoff.ru/purchases/', 'https://www.tinkoff.ru/settings/?auth=null&large=null']
    while True:
        time.sleep(10)
        status, info = check(driver)
        if status == True:
            check_operation(driver, info)
        x += 10
        if x == 500:
            while True:
                link = links[random.randint(0, len(links) - 1)]
                if link != link_now:
                    break
            link_now = link
            driver.get(link_now)
            x = 0


def main():
    driver = first_open()
    wait(driver)

main()
