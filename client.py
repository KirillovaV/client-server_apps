"""
Клиентская часть:
Функции клиента:
сформировать presence-сообщение;
отправить сообщение серверу; - реализовано в utils.py
получить ответ сервера; - реализовано в utils.py
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import json
from time import time
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP


def create_message(user='User', password=''):
    """
    Функция формирует presence-сообщение
    :param user: Имя пользователя
    :param password: Пароль
    :return:
    """
    message = {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'user': {
            'account_name': user,
            'password': password
        }
    }
    return message


def read_response(message):
    """
    Функция принимает ответ сервера и выводит на экран
    соответствующий результат
    :param message:
    :return:
    """
    if 'response' in message:
        if message['response'] == 200:
            return f'200: {message["alert"]}'
        if message['response'] == 400:
            return f'400: {message["error"]}'
    raise ValueError


def run_client():
    """
    Основная функция для запуска клиентской части
    """
    # Получаем порт из аргументов командной строки
    # или назначаем порт по умолчанию
    try:
        connection_port = int(argv[2])
        if not (1024 < connection_port < 65535):
            raise ValueError
    except (IndexError, ValueError):
        connection_port = DEFAULT_PORT

    # Получаем ip-адрес из аргументов командной строки
    # или назначаем по умолчанию
    try:
        connection_ip = argv[1]
    except IndexError:
        connection_ip = DEFAULT_IP

    # Создаем сокет
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((connection_ip, connection_port))

    # Создаем и отправляем сообщение
    message = create_message()
    send_message(client_socket, message)

    try:
        # Получаем и обрабатываем ответ сервера
        answer = read_response(get_message(client_socket))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')

    # Закрываем сокет
    client_socket.close()


if __name__ == '__main__':
    run_client()
