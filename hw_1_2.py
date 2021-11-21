"""
2. Каждое из слов «class», «function», «method» записать в байтовом
типе без преобразования в последовательность кодов (не используя
методы encode и decode) и определить тип, содержимое и длину
соответствующих переменных.
"""

TEST_WORDS = [
    'class',
    'function',
    'method',
]


def word_to_bytes(*args):
    for word in args:
        byte_word = eval(f'b"{word}"')
        print(f'{byte_word} - {type(byte_word)} - {len(byte_word)} символов')


word_to_bytes(*TEST_WORDS)
