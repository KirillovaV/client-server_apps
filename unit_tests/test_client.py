"""
Unit-тесты для модуля client.py
"""

import os
import sys
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presence_message, read_response
from errors import MissingFieldError


class TestClient(unittest.TestCase):
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

    def test_create_message_ok(self):
        """Формирование стандартного сообщения"""
        test_msg = create_presence_message()
        test_msg['time'] = 1

        self.assertEqual(test_msg, {'action': 'presence', 'time': 1, 'type': 'status',
                                    'user': {'account_name': 'User', 'password': ''}})

    def test_create_message_another_user_ok(self):
        """
        Формирование сообщения с другими параметрами пользователя
        Верный результ
        """
        test_msg = create_presence_message(user='Test', password='Test')
        test_msg['time'] = 1

        self.assertEqual(test_msg, {'action': 'presence', 'time': 1, 'type': 'status',
                                    'user': {'account_name': 'Test', 'password': 'Test'}})

    def test_create_message_another_user_error(self):
        """
        Формирование сообщения с другими параметрами пользователя
        Неверный результат
        """
        test_msg = create_presence_message(user='Test', password='Test')
        test_msg['time'] = 1

        self.assertNotEqual(test_msg, {'action': 'presence', 'time': 1, 'type': 'status',
                                       'user': {'account_name': 'User', 'password': ''}})

    def test_create_message_is_dict(self):
        """
        Проверяет, является ли возвращенный объект словарем
        """
        test_msg = create_presence_message()
        self.assertIsInstance(test_msg, dict)

    def test_read_response_200(self):
        """Разбор корректного ответа сервера, успешное соединение"""
        test_resp = read_response(self.correct_response)
        self.assertEqual(test_resp, '200: Соединение прошло успешно')

    def test_read_response_400(self):
        """Разбор корректного ответа сервера, ошибка соединения"""
        test_resp = read_response(self.error_response)
        self.assertEqual(test_resp, '400: Ошибка соединения')

    def test_no_response_1(self):
        """Некорректный ответ сервера"""
        self.assertRaises(MissingFieldError, read_response, {'time': 1, 'error': 'Ошибка соединения'})

    def test_no_response_2(self):
        """Некорректный код ответа"""
        self.assertRaises(ValueError, read_response, {'response': 300})


if __name__ == '__main__':
    unittest.main()
