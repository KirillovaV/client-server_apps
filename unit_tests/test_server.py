"""
Unit-тесты для модуля server.py
"""

import unittest
import os
import sys
from time import time
sys.path.append(os.path.join(os.getcwd(), '..'))
from server import create_response


class TestServer(unittest.TestCase):
    correct_response = {
        'response': 200,
        'time': 1,
        'alert': 'Соединение прошло успешно'
    }
    error_response = {
        'response': 400,
        'time': 1,
        'error': 'Ошибка соединения'
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create_response_ok(self):
        """
        Ответ на корректный запрос
        """
        test_response = create_response({
            'action': 'presence',
            'time': time(),
            'type': 'status',
            'user': {
                'account_name': 'User',
                'password': ''
            }
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.correct_response)

    def test_create_response_action_error(self):
        """
        Некорректное действие
        """
        test_response = create_response({
            'action': 'wrong_action',
            'time': time(),
            'type': 'status',
            'user': {
                'account_name': 'User',
                'password': ''
            }
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.error_response)

    def test_create_response_no_action(self):
        """
        Отсутствие действия
        """
        test_response = create_response({
            'time': time(),
            'type': 'status',
            'user': {
                'account_name': 'User',
                'password': ''
            }
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.error_response)

    def test_create_response_no_time(self):
        """
        Отсутствие временного штампа
        """
        test_response = create_response({
            'action': 'presence',
            'type': 'status',
            'user': {
                'account_name': 'User',
                'password': ''
            }
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.error_response)

    def test_create_response_no_user(self):
        """
        Нет пользователя
        """
        test_response = create_response({
            'action': 'presence',
            'time': time(),
            'type': 'status',
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.error_response)

    def test_create_response_user_error(self):
        """
        Неверный формат поля "user"
        """
        test_response = create_response({
            'action': 'presence',
            'time': time(),
            'type': 'status',
            'user': 'User'
        })
        test_response['time'] = 1
        self.assertEqual(test_response, self.error_response)

    def test_response_is_dict(self):
        """
        Проверяет, является ли возвращенный объект словарем
        """
        test_response = create_response({
            'action': 'presence',
            'time': time(),
            'type': 'status',
            'user': {
                'account_name': 'User',
                'password': ''
            }
        })
        test_response['time'] = 1
        self.assertIsInstance(test_response, dict)


if __name__ == '__main__':
    unittest.main()
