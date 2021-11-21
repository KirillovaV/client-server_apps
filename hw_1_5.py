"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.
"""
import platform
import subprocess
import chardet

# количество пакетов
COUNT = 5
# список адресов
URLS = ['yandex.ru', 'youtube.com']
# команда
CODE = '-n' if platform.system() == 'Windows' else '-c'


def ping_decode(count, code, urls):
    for url in urls:
        args = ['ping', code, str(count), url]
        ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        for line in ping.stdout:
            result = chardet.detect(line)
            print(line.decode(result['encoding']).encode('utf-8').decode('utf-8'))


ping_decode(COUNT, CODE, URLS)
