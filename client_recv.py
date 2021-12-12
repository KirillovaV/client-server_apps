"""
Клиентская часть:
Функции клиента:
сформировать presence-сообщение;
отправить сообщение серверу; - реализовано в utils.py
получить ответ сервера; - реализовано в utils.py
разобрать сообщение сервера;
параметры командной строки скрипта client.py <addr> [<port>]:
addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.


Модуль по умолчанию работает на приём сообщений
"""
import argparse
import json
import logging
import log.client_log_config
from time import time, ctime
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
def create_user_message(message, account_name='User'):
    """
    Функция формирует сообщениепользователя для отправки.
    :param account_name:
    :param message:
    :return:
    """
    message = {
        'action': 'msg',
        'time': time(),
        'from': account_name,
        'message': message
    }
    return message


@Log()
def read_user_message(message):
    """
    Функция обрабатывает полученные сообщения и выводит на экран.
    :param message: Словарь-сообщение
    :return:
    """
    client_log.debug(f'Разбор сообщения сервера: {message}')
    if ('action' in message and message['action'] == 'msg'
            and 'time' in message and 'from' in message
            and 'message' in message):
        print(f'{message["from"]} - {ctime(message["time"])}:\n'
              f'{message["message"]}')
    else:
        raise ValueError


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


@Log()
def get_user_settings():
    """
    Получает порт и ip-адрес сервера из аргументов командной строки
    или назначает по умолчанию
    :return:
    """
    args = argparse.ArgumentParser()
    args.add_argument('address', default=DEFAULT_IP, nargs='?')
    args.add_argument('port', type=int, default=DEFAULT_PORT, nargs='?')
    args.add_argument('-m', '--mode', default='read', nargs='?')
    namespace = args.parse_args(argv[1:])
    connection_ip = namespace.address
    connection_port = namespace.port
    mode = namespace.mode

    if not (1024 < connection_port < 65535):
        client_log.critical(f'Неверное значение порта {connection_port}.\n'
                            f'Порт должен находиться в диапазоне от 1024 до 65535.')
        exit(1)

    if mode not in ('read', 'send'):
        client_log.critical(f'Недопустимый режим запуска {mode}.\n'
                            f'Доступные режимы: "read", "send".')
        exit(1)

    return connection_ip, connection_port, mode


def run_client():
    """
    Основная функция для запуска клиентской части
    """
    client_log.info(f'Запуск клиента.')
    connection_ip, connection_port, mode = get_user_settings()

    try:
        # Создаем сокет
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((connection_ip, connection_port))
        client_log.info(f'Соединение с сервером {connection_ip}:{connection_port}')

        # Создаем и отправляем presence-сообщение
        message = create_presence_message()
        send_message(client_socket, message)
        client_log.info(f'Отрправлено сообщение {message}')

        # Получаем и обрабатываем ответ сервера
        answer = read_response(get_message(client_socket))
        client_log.info(f'Получен ответ сервера {answer}')

    except ConnectionRefusedError:
        client_log.critical(f'Не удалось установить соединение с сервером '
                            f'{connection_ip}:{connection_port}')
        exit(1)

    except (ValueError, NotDictError):
        client_log.error(f'Неверный формат передаваемых данных.')

    except MissingFieldError as err:
        client_log.error(f'Ответ сервена не содержит поля {err.missing_field}')

    except json.JSONDecodeError:
        client_log.error(f'Не удалось декодировать сообщение сервера.')

    # Отправляем сообщение на сервер
    if mode == 'send':
        client_log.info(f'Клиент запущен в режиме отпраки сообщений.')
        print(f'Клиент запущен в режиме отпраки сообщений.')
        while True:
            msg = input('Введите сообщение для отправки или "exit" для выхода: ')
            message = create_user_message(msg)
            send_message(client_socket, message)
            client_log.info(f'Отрправлено сообщение {message}')
            if msg == 'exit':
                break

    # Получаем отправленные сообщения
    elif mode == 'read':
        client_log.info(f'Клиент запущен в режиме получения сообщений.')
        print(f'Клиент запущен в режиме получения сообщений.')
        while True:
            answer = read_user_message(get_message(client_socket))
            client_log.info(f'Получено сообщение {answer}')


    # Закрываем сокет
    client_socket.close()
    client_log.info('Завершение подключения.')


if __name__ == '__main__':
    run_client()
