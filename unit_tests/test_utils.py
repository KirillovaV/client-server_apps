"""
Unit-тесты для модуля utils.py
"""

import json
import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from common.utils import get_message, send_message


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestUtils(unittest.TestCase):
    test_message = {
        'action': 'presence',
        'time': 1,
        'type': 'status',
        'user': {
            'account_name': 'User',
            'password': ''
        }
    }
    test_correct_response = {
        'response': 200,
        'time': 1,
        'alert': 'Соединение прошло успешно'
    }
    test_error_response = {
        'response': 400,
        'time': 1,
        'error': 'Ошибка соединения'
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_send_message(self):
        test_socket = TestSocket(self.test_message)
        send_message(test_socket, self.test_message)
        self.assertEqual(test_socket.encoded_message, test_socket.received_message)
        self.assertRaises(TypeError, send_message, test_socket, 'wrong dict')

    def test_get_message(self):
        test_sock_ok = TestSocket(self.test_correct_response)
        test_sock_err = TestSocket(self.test_error_response)
        # Корректная расшифровка корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_correct_response)
        # Корректная расшифровка ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_error_response)


if __name__ == '__main__':
    unittest.main()
