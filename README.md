```
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
```

**LocalChat** - клиент-серверная программа, типо мессенджера.

У меня получилось так что когда первый клиент отправляет сообщение, то этот же клиент сможет отправить сообщение только после того, как ему ответит второй клиент (а я хотел чтобы одновременно можно было отправлять и принимать сообщения : /)

В чате есть 2 команды:
- `cmd:closeconn` - закрывает соединение
- `cmd:sendfile` - отправить файл
  
Также поясню за конфиг файл:
- `anonymousMod` `[true/false]`: скрывать имя компьютера в чате
- `useIPVer` `[4/6]`: использовать IPv4 или IPv6
- `bufSize` `[число]`: размер буфера для сообщений
- `bufSizeForTransferFiles` `[число]`: размер буфера для передачи файлов
- `dynamicChoicePort` `[true/false]`: динамический выбор порта для создания подключения
- `dynamicChoicePort_portRange_begin` `[число]`: начальный порт для параметра `dynamicChoicePort`
- `dynamicChoicePort_portRange_end` `[число]`: конечный порт для параметра `dynamicChoicePort`
- `portForFunc__getip_server_client` `[число]`: порт для функций `__getip_server` и `__getip_client`
- `dynamicChoicePortForFunc__getip_server_client` `[true/false]`: динамический выбор порта для функций `__getip_server` и `__getip_client`
- `dynamicChoicePortForFunc__getip_server_client_portRange_begin` `[число]`: начальный порт для параметра `portForFunc__getip_server_client`
- `dynamicChoicePortForFunc__getip_server_client_portRange_end` `[число]`: конечный порт для параметра `portForFunc__getip_server_client`