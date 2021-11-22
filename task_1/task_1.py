"""
1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt,
info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных
данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить
в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import re
from chardet import detect

FILE_LIST = ['info_1.txt', 'info_2.txt', 'info_3.txt']
CSV_FILE = 'mani_data.csv'


def get_data(csv_file_name, data_files):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    for file in data_files:
        with open(file, 'rb') as f:
            content = f.read()
        content = content.decode(detect(content)['encoding'])
        line1 = re.search('(?<=(Изготовитель системы:)).*?(?=\n)', content)
        os_prod_list.append(line1.group(0).strip())
        line2 = re.search('(?<=(Название ОС:)).*?(?=\n)', content)
        os_name_list.append(line2.group(0).strip())
        line3 = re.search('(?<=(Код продукта:)).*?(?=\n)', content)
        os_code_list.append(line3.group(0).strip())
        line4 = re.search('(?<=(Тип системы:)).*?(?=\n)', content)
        os_type_list.append(line4.group(0).strip())

    with open(csv_file_name, 'w', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        file_writer.writerow(main_data)

    return os_prod_list, os_name_list, os_code_list, os_type_list


def write_to_csv(file_name):
    data = get_data(file_name, FILE_LIST)
    data = list(zip(*data))
    with open(file_name, 'a', encoding='utf-8') as file:
        file_writer = csv.writer(file)
        file_writer.writerows(data)


write_to_csv(CSV_FILE)
