"""
3. Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.

Для этого:
Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список,
второму — целое число, третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);

Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml

DATA = {
    1: ['раз', 'два', 'три'],
    2: 10,
    3: {'1€': 'some_data',
        '4$': 'ещё данные'}
}
FILE_NAME = 'file.yaml'


def write_to_yaml(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True, sort_keys=False)


write_to_yaml(FILE_NAME, DATA)

with open(FILE_NAME, encoding='utf-8') as file:
    content = yaml.load(file, Loader=yaml.FullLoader)
print(f'Исходные данные {DATA}')
print(f'Данные из файла {content}')
