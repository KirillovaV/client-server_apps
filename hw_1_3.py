"""
3. Определить, какие из слов «attribute», «класс», «функция»,
«type» невозможно записать в байтовом типе.
"""

TEST_WORDS = [
    'attribute',
    'класс',
    'функция',
    'type',
]


def bytes_encoding(word):
    try:
        print(word.encode('ascii'))
    except UnicodeEncodeError:
        print(f'Слово "{word}" невозможно записать в байтовом типе')


for word in TEST_WORDS:
    bytes_encoding(word)
