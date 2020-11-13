import ast
import random


def update_bd(info, option, id):
    with open('bd_id.txt', 'r', encoding='UTF-8') as x:
        f = x.read().split('\n')
        x.close()
    fl = False

    try:
    #if True:
        for i in range(len(f)):
            try:
                if f[i] == '':
                    continue
                f[i] = ast.literal_eval(f[i])
                if str(f[i]['id']) == str(id):
                    f[i][option] = info
                    fl = True
                    break
            except Exception:
                pass
    except Exception:
        pass
    if fl:
        with open('bd_id.txt', 'w', encoding='UTF-8') as x:
            for i in f:
                x.write(str(i))
                x.write('\n')
            x.close()
    if not fl:
        with open('bd_id.txt', 'a', encoding='UTF-8') as f:
            f.write('\n')
            f.write(str({'id': str(id), option: info}))
            f.close()


def get_user_info_bd(id):
    with open('bd_id.txt', 'r', encoding='UTF-8') as f:
        f = f.read().split('\n')
    fl = False
    try:
        for i in range(len(f)):
            try:
                f[i] = ast.literal_eval(f[i])
                if f[i]['id'] == str(id):
                    return '1', f[i]
            except Exception:
                pass
    except Exception:
        pass
    return '0', ''


def generate_keyword():
    alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
    fl = True
    while fl:
        password = ''
        for i in range(7):
            password += alphabet[random.randint(0, len(alphabet) - 1)]
        with open('keywords.txt', 'r', encoding='UTF-8') as f:
            x = f.read().split('\n')
            f.close()
            if password not in x:
                fl = False
    with open('keywords.txt', 'a', encoding='UTF-8') as f:
        f.write('\n')
        f.write(str(password))
        f.close()
    return password
