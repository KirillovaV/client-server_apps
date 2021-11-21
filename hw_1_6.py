"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор». Проверить
кодировку файла по умолчанию. Принудительно открыть файл в
формате Unicode и вывести его содержимое.
"""
import chardet

LINES = ['сетевое программирование',
         'сокет',
         'декоратор']

FILE_NAME = 'test_file.txt'

# записываем тестовый файл в кодировке по умолчанию
with open(FILE_NAME, 'w') as file:
    for line in LINES:
        file.write(f'{line}\n')


def unicode_file_decoder(file_name):
    # определяем кодировку файла
    with open(file_name, 'rb') as file:
        file_content = file.read()
    file_enc = chardet.detect(file_content)['encoding']
    print(f'Кодировка {file_enc}')
    text = file_content.decode(file_enc)

    # перезаписываем файл в unicode
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)

    # открываем файл в unicode
    with open(FILE_NAME, encoding='utf-8') as file:
        file_content = file.read()
    print(file_content)


unicode_file_decoder(FILE_NAME)
