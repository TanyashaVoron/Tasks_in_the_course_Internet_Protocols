# Задачи по курсу «Протоколы Интернета»
1. Стоимость = 10 баллов.
    * Трассировка автономных систем. Пользователь вводит доменное имя
    или IP адрес. Осуществляется трассировка до указанного узла, т. е. мы узнаем IP адреса маршрутизаторов, через которые проходит пакет. 
    * Определяет к какой автономной системе относится каждый из полученных IP адресов
    маршрутизаторов, для этого обращается к базам данных региональных интернет регистраторов.
    * Выход: для каждого IP-адреса – результат трассировки (или кусок результата до появления ***), 
    * для "белых" IP-адресов из него указать номер автономной системы.
    * В итоге должна получиться таблица № по порядку IP AS страна и провайдер.
2. 
3. 
4. Стоимость = 20 баллов. 
    * Кэширующий DNS сервер. 
    * Сервер прослушивает 53 порт. При первом запуске кэш пустой. 
    * Сервер получает от клиента рекурсивный запрос и выполняет разрешение запроса. 
    * Получив ответ, сервер разбирает пакет ответа, извлекает из него ВСЮ полезную информацию, т. е. все ресурсные записи, а не только то, 
    о чем спрашивал клиент. Полученная информация сохраняется в кэше сервера. Например, это может быть два хэш-массива.
    * Сервер регулярно просматривает кэш и удаляет просроченные записи (использует поле TTL).
    * Сервер не должен терять работоспособность (уходить в бесконечное ожидание, падать с
    ошибкой и т. д.), если старший сервер почему-то не ответил на запрос. 
    * Во время штатного выключения сервер сериализует данные из кэша, сохраняет их на диск. 
    * При повторных запусках
    сервер считывает данные с диска и удаляет просроченные записи, инициализирует таким образом свой кэш.
5. 
6. 
7. 
8. 
