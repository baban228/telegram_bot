import os
from fuzzywuzzy import fuzz
mas = []

if os.path.exists('phrase_list.txt'):
    f = open('phrase_list.txt', 'r', encoding='UTF-8')
    for x in f:
        if (len(x.strip()) > 2):
            mas.append(x.strip().lower())
    f.close()


def answer(text):
    try:
        text = text.lower().strip()
        if os.path.exists('phrase_list.txt'):
            a = 0
            n = 0
            nn = 0
            for q in mas:
                if ('u: ' in q):
                    aa = (fuzz.token_sort_ratio(q.replace('u: ', ''), text))
                    if (aa > a and aa != a):
                        a = aa
                        nn = n
                n = n + 1
            s = mas[nn + 1]
            return s
        else:
            return 'Круто!'
    except:
        return 'Круто!'


def speake(context, chat_id):
    f = open("logs/" + str(chat_id) + '_CLStore_log.txt', 'a', encoding='UTF-8')
    s = answer(context)
    f.write('u: ' + context + '\n' + s + '\n')
    f.close()
    return s