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
import logging
import log.server_log_config
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_LISTEN_ADDRESSES, MAX_USERS
from decos import Log
from errors import NotDictError

server_log = logging.getLogger('server')


@Log()
def create_response(message):
    """
    Функция проверяет поля сообщения на соответствие JIM-формату
    и формирует ответное сообщение с кодом ответа.
    :param message: сообщение в виде словаря
    :return: ответ в виде словаря
    """
    server_log.debug(f'Формирование ответа на сообщение {message}')
    if ('action' in message and message['action'] == 'presence'
            and 'time' in message and 'user' in message
            and isinstance(message['user'], dict)):
        return {
            'response': 200,
            'time': time(),
            'alert': 'Соединение прошло успешно'
        }
    return {
        'response': 400,
        'time': time(),
        'error': 'Ошибка соединения'
    }


def run_server():
    """
    Основная функция для запуска сервера
    """
    server_log.info('Запуск сервера.')

    # Проверяем наличие в аргументах запуска порта для работы
    # или назначаем порт по умолчанию
    if '-p' in argv:
        try:
            listen_port = int(argv[argv.index('-p') + 1])
            if not (1024 < listen_port < 65535):
                raise ValueError
        except IndexError:
            server_log.error('За параметром "-p" должен следовать номер порта.')
            listen_port = DEFAULT_PORT
            server_log.info('Назначен порт по умолчанию.')
        except ValueError:
            server_log.error(f'Неверное значение порта {listen_port}.'
                             f'Назначен порт по умолчанию.')
            listen_port = DEFAULT_PORT
    else:
        listen_port = DEFAULT_PORT

    # Проверяем наличие в аргументах IP-адреса для прослушивания
    # или назначаем для прослушивания все доступные адреса
    if '-a' in argv:
        try:
            listen_addr = argv[argv.index('-a') + 1]
        except IndexError:
            server_log.info('Неверные параметры IP-адреса. Будет назначен адрес по умолчанию.')
            listen_addr = DEFAULT_LISTEN_ADDRESSES
    else:
        listen_addr = DEFAULT_LISTEN_ADDRESSES

    # Создаём сокет и начинаем прослушивание
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((listen_addr, listen_port))
    server_socket.listen(MAX_USERS)
    server_log.info(f'Сервер запущен. Прослушиваемые адреса: {listen_addr}'
                    f'Порт подключения: {listen_port}')

    while True:
        # Получаем данные клиента
        client, client_address = server_socket.accept()
        server_log.info(f'Установлено соединение клиентом {client_address}')
        try:
            # Получаем сообщение
            incoming_message = get_message(client)
            server_log.info(f'Принято сообщение {incoming_message} '
                            f'от: {incoming_message["user"]["account_name"]}')
            # Обрабатываем сообщение и отправляем ответ
            response = create_response(incoming_message)
            server_log.info(f'Сформирован ответ для клиента {client_address}')
            send_message(client, response)
            server_log.info(f'Отправлено сообщение {response}')

        except (ValueError, NotDictError):
            server_log.error(f'Неверный формат передаваемых данных.')

        except json.JSONDecodeError:
            server_log.error(f'Не удалось декодировать сообщение клиента.')

        finally:
            # Закрываем соединение
            client.close()
            server_log.info(f'Завершение соединения с {client_address}')


if __name__ == '__main__':
    run_server()
