"""
4. Преобразовать слова «разработка», «администрирование»,
«protocol», «standard» из строкового представления в байтовое и
выполнить обратное преобразование (используя методы encode и decode).
"""

TEST_WORDS = [
    'разработка',
    'администрирование',
    'protocol',
    'standard',
]


def word_enc_dec(*args):
    for word in args:
        enc_word_bytes = word.encode('utf-8')
        print(enc_word_bytes)
        enc_word = enc_word_bytes.decode('utf-8')
        print(enc_word)
        print()


word_enc_dec(*TEST_WORDS)
