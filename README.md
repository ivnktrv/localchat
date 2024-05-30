
**LocalChat** - клиент-серверная программа, типо мессенджера.

У меня получилось так что когда первый клиент отправляет сообщение, то этот же клиент сможет отправить сообщение только после того, как ему ответит второй клиент (а я хотел чтобы одновременно можно было отправлять и принимать сообщения : /)

**И да, прога работает в пределах локальной сети : /**

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
- 
***

### Хотите внести свой вклад в проект? - читайте [CONTRIBUTING.md](CONTRIBUTING.md)

***