"""
Серверная часть.
Функции сервера:
принимает сообщение клиента; - реализовано в utils.py
формирует ответ клиенту;
отправляет ответ клиенту; - реализовано в utils.py
имеет параметры командной строки:
    -p <port> — TCP-порт для работы (по умолчанию использует 7777);
    -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""
import json
from time import time
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_LISTEN_ADDRESSES, MAX_USERS


def create_response(message):
    """
    Функция проверяет поля сообщения на соответствие JIM-формату
    и формирует ответное сообщение с кодом ответа.
    :param message:
    :return:
    """
    if ('action' in message and message['action'] == 'presence'
            and 'time' in message and 'user' in message):
        return {
            'response': 200,
            'time': time(),
            'alert': 'Соединение прошло успешно'
        }
    return {
        'response': 400,
        "time": time(),
        'error': 'Ошибка соединения'
    }


def run_server():
    """
    Основная функция для запуска сервера
    """
    # Проверяем наличие в аргументах запуска порта для работы
    # или назначаем порт по умолчанию
    if '-p' in argv:
        try:
            listen_port = int(argv[argv.index('-p') + 1])
            if not (1024 < listen_port < 65535):
                raise ValueError
        except (IndexError, ValueError):
            print('Неверные параметры порта. Будет назначен порт по умолчанию.')
            listen_port = DEFAULT_PORT
    else:
        listen_port = DEFAULT_PORT

    # Проверяем наличие в аргументах IP-адреса для прослушивания
    # или назначаем для прослушивания все доступные адреса
    if '-a' in argv:
        try:
            listen_addr = argv[argv.index('-a') + 1]
        except IndexError:
            print('Неверные параметры IP-адреса. Будет назначен адрес по умолчанию.')
            listen_addr = DEFAULT_LISTEN_ADDRESSES
    else:
        listen_addr = DEFAULT_LISTEN_ADDRESSES

    # Создаём сокет и начинаем прослушивание
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((listen_addr, listen_port))
    server_socket.listen(MAX_USERS)

    while True:
        # Получаем данные клиента
        client, client_address = server_socket.accept()
        try:
            # Получаем сообщение
            incoming_message = get_message(client)
            print(f'Принято presence-сообщение от: {incoming_message["user"]["account_name"]}')
            # Обрабатываем сообщение и отправляем ответ
            response = create_response(incoming_message)
            send_message(client, response)
            # Закрываем соединение
            client.close()
        except (ValueError, json.JSONDecodeError):
            print('Ошибка чтения сообщения')
            client.close()


if __name__ == '__main__':
    run_server()
