"""
Этот скрипт создает строку с правильным библиографическим содержанием для ссылок на интернет-ресурсы согласно национальному стандарту РФ ГОСТ Р 7.0.100-2018 «Библиографическая запись. Библиографическое описание. Общие требования и правила составления».

(c) tankalxat34 - 2022
Version: 0.1.2
-----------------------------------------------------------------------------------------------------------------------
"""
import time, os, requests, re
from urllib.parse import unquote
os.system("cls")

HEADERS = {"user-agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.2"}
COMMENT_SYMBOL = ";"
COUNTER = 1
ABC = "0123456789абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"
BIBLIOLINKS_LIST = []

print(__doc__)

TEMPLATE = "{title} — Текст: электронный // {domen}: [сайт]. — URL: {url} (дата обращения: {date})."
_date = time.strftime("%d.%m.20%y")

file_with_links = input("Введите имя файла, где находятся ссылки, или нажмите Return, чтобы использовать `%s` \n\tОбратите внимание, что каждая ссылка должна быть написана на каждой строке подряд: " % ("links.txt"))
if file_with_links == "":
    file_with_links = "links.txt"

try:
    input_strings = open(file_with_links.replace('"', ""), "r", encoding="utf-8").readlines()
except Exception:
    print("Такого файла нет. Попробуйте еще раз")
    quit()

print("Обработка ссылок началась. Результат откроется сразу после окончания работы. Пожалуйста, подождите...")

try:
    os.remove("result.txt")
except Exception:
    pass

f = open("result.txt", "a", encoding="utf-8")

for link in input_strings:
    local_link = unquote(link.strip())

    if local_link == COMMENT_SYMBOL:
        continue
    print(COUNTER, "Формирование источника для:\t\t", local_link, end=" ... ")

    
    try:
        req = requests.get(local_link, headers=HEADERS)
        try:
            _title = re.findall('<title>(.+?)</title>', req.text)[0] +'.'
        except Exception:
            _title='.'
        try:
            _author = re.findall("[аА]втор[:ы].[аА-яЯ]{0,}.[аА-яЯ]{0,}..[аА-яЯ]{0,}.", req.text)[0]
            _author2 = "/ "+re.findall("[аА]втор[:ы].[аА-яЯ]{0,}.[аА-яЯ]{0,}..[аА-яЯ]{0,}.", req.text)[0]+"."
        except Exception:
            _author = ' '
            _author2 = ' '
        _domen = local_link.split("/")[2].replace("www.", "", 1)
        _url = local_link

        BIBLIOLINKS_LIST.append((TEMPLATE.format(author=_author,
                                 author2=_author2,
                                title=_title,
                                domen=_domen,
                                url=_url,
                                date=_date)).strip())
        print("\033[92mУспешно!\033[0m\n")
    except Exception:
        print("\033[91mВозникла ошибка при формировании источника...\033[0m")
    COUNTER += 1

print("\n\n")

COUNTER = 0
BIBLIOLINKS_LIST.sort()
for e in BIBLIOLINKS_LIST:
    print(COUNTER + 1, "Запись в файл источника:", e)
    f.write(e)
    f.write("\n"*1)
    COUNTER += 1

f.close()

os.system("explorer.exe "+os.getcwd()+"\\result.txt")
