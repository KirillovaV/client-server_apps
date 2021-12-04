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
import logging
import log.client_log_config
from time import time
from sys import argv
from socket import socket, AF_INET, SOCK_STREAM
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP
from decos import Log
from errors import NotDictError, MissingFieldError

client_log = logging.getLogger('client')


@Log()
def create_presence_message(user='User', password=''):
    """
    Функция формирует presence-сообщение
    :param user: Имя пользователя
    :param password: Пароль
    :return:
    """
    client_log.debug(f'Создание приветственного сообщения серверу от {user}')
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


@Log()
def read_response(message):
    """
    Функция принимает ответ сервера и выводит на экран
    соответствующий результат
    :param message:
    :return:
    """
    client_log.debug(f'Разбор ответа сервера: {message}')
    if 'response' in message:
        if message['response'] == 200:
            return f'200: {message["alert"]}'
        elif message['response'] == 400:
            return f'400: {message["error"]}'
        else:
            raise ValueError
    raise MissingFieldError('response')


def run_client():
    """
    Основная функция для запуска клиентской части
    """
    client_log.info(f'Запуск клиента.')

    # Получаем порт из аргументов командной строки
    # или назначаем порт по умолчанию
    try:
        connection_port = int(argv[2])
        if not (1024 < connection_port < 65535):
            raise ValueError
    except IndexError:
        client_log.info(f'Не получен порт назначения. Присвоено значение по умолчанию.')
        connection_port = DEFAULT_PORT
    except ValueError:
        client_log.critical(f'Неверное значение порта {connection_port}.\n'
                            f'Порт должен находиться в диапазоне от 1024 до 65535.')
        exit(1)

    # Получаем ip-адрес из аргументов командной строки
    # или назначаем по умолчанию
    try:
        connection_ip = argv[1]
    except IndexError:
        client_log.info(f'Не получен IP-адрес сервера. Присвоено значение по умолчанию.')
        connection_ip = DEFAULT_IP

    try:
        # Создаем сокет
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((connection_ip, connection_port))
        client_log.info(f'Соединение с сервером {connection_ip}:{connection_port}')

        # Создаем и отправляем сообщение
        message = create_presence_message()
        send_message(client_socket, message)
        client_log.info(f'Отрправлено сообщение {message}')

        # Получаем и обрабатываем ответ сервера
        answer = read_response(get_message(client_socket))
        client_log.info(f'Получен ответ сервера {answer}')

    except ConnectionRefusedError:
        client_log.critical(f'Не удалось установить соединение с сервером '
                            f'{connection_ip}:{connection_port}')

    except (ValueError, NotDictError):
        client_log.error(f'Неверный формат передаваемых данных.')

    except MissingFieldError as err:
        client_log.error(f'Ответ сервена не содержит поля {err.missing_field}')

    except json.JSONDecodeError:
        client_log.error(f'Не удалось декодировать сообщение сервера.')

    # Закрываем сокет
    client_socket.close()
    client_log.info(f'Завершение подключения.')


if __name__ == '__main__':
    run_client()
