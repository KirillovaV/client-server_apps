"""
Лаунчер
Запускает сервер, 2 клиента на отправку сообщений и 2 клиента на приём сообщений
"""

from subprocess import Popen, CREATE_NEW_CONSOLE


# Запускаемые процессы
processes = []

while True:
    command = input("Запустить сервер и клиентов (s) / Закрыть все окна и выйти (q) ")

    if command == 'q':
        for proc in processes:
            proc.kill()
        processes.clear()
        break

    elif command == 's':
        # Запустить сервер
        processes.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))

        # Запустить 2 клиента на отправку сообщений
        for i in range(2):
            processes.append(Popen('python client.py -m send', creationflags=CREATE_NEW_CONSOLE))

        # Запустить 2 клиента на приём сообщений
        for i in range(2):
            processes.append(Popen('python client.py -m read', creationflags=CREATE_NEW_CONSOLE))
