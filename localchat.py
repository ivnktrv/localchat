LOGO = '''
                                                      _______
    __         ______   ______   ________  __         | ... |            ______  __    __   ________  __________
    | |       /  __  \ /  ____| /  ____  \ | |        |____ |           /  ____| | |   | | /  ____  \ |___   ___|
    | |       | |  | | | |      | |____| | | |             \|    _____  | |      | |___| | | |____| |     | |
    | |       | |  | | | |      |  ____  | | |                ___|   |  | |      | ____  | |  ____  |     | |
    | |       | |  | | | |      | |    | | | |               /   ¯¯|¯¯  | |      | |   | | | |    | |     | |
    | |_____  | |__| | | |____  | |    | | | |_____   _____ /     ¯¯¯   | |____  | |   | | | |    | |     | |
    |_______| \______/ \______| |_|    |_| |_______|  |   |/            \______| |_|   |_| |_|    |_|     |_|
                                                      ¯¯|¯¯
                                                       ¯¯¯
'''

from random import randint as r
from threading import Thread
from time import sleep
import socket
import json
import sys
import os

try:
    with open('LC_config.json','r') as configFile:
        configFile = json.load(configFile)
except FileNotFoundError:
    data = {
    "1":"          BASIC OPTIONS          ",

    "anonymousMod": False,
    "useIPVer": 4,
    "bufSize": 4096,
    "bufSizeForTransferFiles": 256,
    
    "2":"          SERVER OPTIONS          ",
    
    "dynamicChoicePort": False,
    "dynamicChoicePort_portRange_begin": 50000,
    "dynamicChoicePort_portRange_end": 65535,

    "3":"          OTHER OPTIONS          ",

    "portForFunc__getip_server_client": 65534,
    "dynamicChoicePortForFunc__getip_server_client": True,
    "dynamicChoicePortForFunc__getip_server_client_portRange_begin": 50000,
    "dynamicChoicePortForFunc__getip_server_client_portRange_end": 65535
    }
    with open('LC_config.json','w') as writeConfigFile:
        json.dump(data, writeConfigFile, indent=4)
    input('[-] Файл конфигурации не был найден, поэтому он был создан')
    exit()

def __clearTerminal():
    if sys.platform == 'win32': os.system('cls')
    else: os.system('clear')

#----------------------------------------------
usedPort = 0
flag = False
def __getip_server(ipver: int):
    global usedPort
    global flag
    if ipver == 4: server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif ipver == 6: server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if configFile["dynamicChoicePortForFunc__getip_server_client"] is False:
        try: server.bind((socket.gethostname(), configFile["portForFunc__getip_server_client"]))
        except Exception as e:
            input(f'[-] Ошибка в функции __getip_server: {e}')
        server.listen()
        addr = server.accept()[1]
        server.close()
        return addr[0]
    else:
        port = configFile["dynamicChoicePortForFunc__getip_server_client_portRange_begin"]
        while port <= configFile["dynamicChoicePortForFunc__getip_server_client_portRange_end"]:
            port += 1
            usedPort = port
            try:
                server.bind((socket.gethostname(), port))
                flag = True
                server.listen()
                addr = server.accept()[1]
                server.close()
                return addr[0]
                
            except OSError:
                continue
def __getip_client(ipver: int):
    if ipver == 4: server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif ipver == 6: server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if configFile["dynamicChoicePortForFunc__getip_server_client"] is False:
        server.connect((socket.gethostname(), configFile["portForFunc__getip_server_client"]))
        server.close()
    else:
        while True:
            if flag is True:
                try: server.connect((socket.gethostname(), usedPort))
                except Exception as e:
                    input(f'[-] Ошибка в функции __getip_client: {e}')
                server.close()
                break       
def getIPv4():
    Thread(target=__getip_client, args=(4,)).start()
    return __getip_server(4)
def getIPv6():
    Thread(target=__getip_client, args=(6,)).start()
    return __getip_server(6)
#----------------------------------------------

while True:
    def __sendFile(__socket):
        print('\n! СОЕДИНЕНИЕ БУДЕТ РАЗОРВАНО !\n')
        getNameExp = input('Укажите файл (с расширением) > ')
        try: file = open(f'{getNameExp}','rb')
        except FileNotFoundError:
            input('[-] Файл не найден')
            exit()
        __socket.send('op:getreadychars'.encode('UTF-8'))
        print('[...] Ожидание готовности клиента')
        while True:
            isReady = __socket.recv(configFile["bufSizeForTransferFiles"]).decode('UTF-8')
            if isReady == 'cond:ready':
                print(f'[...] Отправка данных. Размер буфера: {configFile["bufSizeForTransferFiles"]} байт')
                chars = file.read(configFile["bufSizeForTransferFiles"])
                while chars:
                    __socket.send(chars)
                    chars = file.read(configFile["bufSizeForTransferFiles"])
                file.close()
                __socket.close()
                input('[+] Сделано. Нажмите на Enter, чтобы закрыть соединение')
                break

    def __getFile(__socket):
        print('\n! СОЕДИНЕНИЕ БУДЕТ РАЗОРВАНО !\n')
        getNameExp = input('Сохранить файл как... > ')
        if os.path.exists('LC_files') is False: os.mkdir('LC_files')
        file = open(f'LC_files/{getNameExp}','wb')
        __socket.send('cond:ready'.encode('UTF-8'))
        print(f'[...] Получение данных. Размер буфера: {configFile["bufSizeForTransferFiles"]} байт')
        while True:
            chars = __socket.recv(configFile["bufSizeForTransferFiles"])
            file.write(chars)
            if not chars: break
        file.close()
        __socket.close()
        input('[+] Сделано. Нажмите на Enter, чтобы закрыть соединение')

    def __sendMsg(__socket):
        try:
            msg = input(f'{socket.gethostname()} > ')
            match msg:
                case 'cmd:closeconn':
                    __socket.send('cmd:closeconn'.encode('UTF-8'))
                    return False
                case 'cmd:sendfile':
                    __sendFile(__socket)
    
        except KeyboardInterrupt: return False
        try:
            match configFile['anonymousMod']:
                case False: __socket.send(f'{socket.gethostname()} > {msg}'.encode('UTF-8'))
                case True: __socket.send(f'??? > {msg}'.encode('UTF-8'))
                case _:
                    input('\n[-] Неверное значение anonymousMode в LC_config.json')
                    return False
        except (ConnectionResetError, ConnectionRefusedError):
            input('\n[-] Удалённый хост принудительно разорвал существующее подключение')
            __socket.close()
            return False
        except Exception as e:
            input(f'[-] Ошибка: {e}')
            __socket.close()
            return False

    def __recieveMsg(__socket):
        try:
            data = __socket.recv(configFile["bufSize"]).decode('UTF-8')
            if data == 'cmd:closeconn':
                input('\n[-] Клиент разорвал соединение')
                return False
            if data == 'op:getreadychars':
                __getFile(__socket)
                return False
        except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            input('\n[-] Клиент разорвал соединение')
            return False
        if not data: pass
        print(data)

    def _matrixEffect():
        print(f'{r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} {r(0,1)}{r(0,1)}{r(0,1)}{r(0,1)} ')
        sleep(0.05)

    def _server():
        __clearTerminal()
        if configFile["useIPVer"] == 4: server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif configFile["useIPVer"] == 6: server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            input('[-] Указана неизвестная версия IP в LC_config.json')
            exit()

        getHost = socket.gethostname()
        if configFile["dynamicChoicePort"] is False:
            try:
                getPort = int(input('Порт (1 - 65535) -> '))
            except ValueError: input('Вы должны указать число!')
        
            try: server.bind((getHost, getPort))
            except Exception as e: input(f'\n[-] Ошибка: {e}')
        else:
            port = configFile["dynamicChoicePort_portRange_begin"]
            while port <= configFile["dynamicChoicePort_portRange_end"]:
                try:
                    server.bind((getHost, port))
                    break
                except OSError:
                    port += 1
                    continue

        server.listen()

        __clearTerminal()

        print(f'\n### ИМЯ ВАШЕГО КОМПЬЮТЕРА: {socket.gethostname()}, IP: {getIPv4() if configFile["useIPVer"]==4 else getIPv6()}, ПОРТ: {getPort if configFile["dynamicChoicePort"] is False else port} ###\n')
        print(f'[?] Включена анонимность?: {configFile["anonymousMod"]}\n[i] Размер буфера: {configFile["bufSize"]} байт\n[i] Версия IP: {configFile["useIPVer"]}\n')
        print('[...] Ожидание подключения')
        try:
            conn, addr = server.accept()
        except KeyboardInterrupt:
            pass
        try:
            if configFile["anonymousMod"] is False:
                conn.send(f'[+] Установлено подключение. Хост: {socket.gethostname()}, IP: {getIPv4() if configFile["useIPVer"]==4 else getIPv6()}, Порт: {getPort if configFile["dynamicChoicePort"] is False else port}\n'.encode('UTF-8'))
            elif configFile["anonymousMod"] is True:
                conn.send(f'[+] Установлено подключение\n'.encode('UTF-8'))
        except FileNotFoundError:
            input('\n[-] Файл LC_getip.py не найден!')
            exit()
        if configFile["anonymousMod"] is False: print(f'[+] Подключён клиент. IP: {addr[0]}\n')
        else: print('[+] Подключён клиент\n')

        while True:
            rcv = __recieveMsg(conn)
            if rcv is False: break
            snd = __sendMsg(conn)
            if snd is False: break
        conn.close()

    def _client():
        __clearTerminal()

        if configFile["useIPVer"] == 4: server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif configFile["useIPVer"] == 6: server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            input('[-] Указана неизвестная версия IP в LC_config.json')
            exit()

        HOST = input('IP -> ')
        while True:
            try:
                PORT = int(input('Порт (1 - 65535) -> ')) # max: 65535
                break
            except ValueError:
                input('Вы должны указать число!')
                continue
        try:
            server.connect((HOST, PORT))
        except socket.gaierror: input('\n[-] Данный хост не найден')   
        except ConnectionRefusedError: input('\n[-] Подключение не установленно, т.к. данный хост слушает другой порт или он не в сети')
        except Exception as e: input(f'\n[-] Ошибка: {e}')
        
        __clearTerminal()

        try:
            print(f'\n### ИМЯ ВАШЕГО КОМПЬЮТЕРА: {socket.gethostname()}, IP: {getIPv4() if configFile["useIPVer"]==4 else getIPv6()} ###\n')
            print(f'[?] Включена анонимность?: {configFile["anonymousMod"]}\n[i] Размер буфера: {configFile["bufSize"]} байт\n[i] Версия IP: {configFile["useIPVer"]}\n')
        except FileNotFoundError:
            input('\n[-] Файл LC_getip.py не найден!')
            exit()

        while True:
            rcv = __recieveMsg(server)
            if rcv is False: break
            snd = __sendMsg(server)
            if snd is False: break
        server.close()

    __clearTerminal()

    print(LOGO)
    try: action = int(input('''
Что сделать?
    
    1: Создать канал
    2: Поключиться к существующему каналу
    3: Получить свой IP

> '''))
    except ValueError:
        __clearTerminal()
        continue
    match action:
        case 1: _server()
        case 2: _client()
        case 3: input(f'\nВаш IPv{configFile["useIPVer"]}: {getIPv4() if configFile["useIPVer"]==4 else getIPv6()}')
        case 0:
            while True:
                try: _matrixEffect()
                except KeyboardInterrupt: break
        case _:
            __clearTerminal()
            continue