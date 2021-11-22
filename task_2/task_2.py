"""
2. Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).
Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;

Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""

import json

FILE_NAME = 'orders.json'


def write_order_to_json(item, quantity, price, buyer, date):
    data = {'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': date}

    with open(FILE_NAME,  encoding='utf-8') as file:
        content = json.load(file)

    content['orders'].append(data)
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


write_order_to_json('item_1', 10, 100.00, 'Иванов', '01.09.2021')
write_order_to_json('item_2', 25, 1000.00, 'Петров', '10.10.2021')
write_order_to_json('item_3', 1, 5150.00, 'Сидоров', '25.10.2021')
