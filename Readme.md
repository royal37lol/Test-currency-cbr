Микросервис для предоставления разницы курса валют относительно рубля.
Реализован на фреймворке Python Flusk.
Данные о курсе валют брались с https://www.cbr.ru/development/SXML/ при помощи библиотеки requests.
Для парсинга XML использовался модуль xml.etree.ElementTree стандартной библиотеки Python.
При запуске приложения список доступных для использования валют кешируется и храниться в виде словаря {'Символьный код валюты': 'Название валюты'},
для того, чтобы не отправлять запрос каждый раз при вызове метода.
Реализованы два метода:
1)availabeCurrency - метод возвращает список валют доступных для использования. Список берется из кешированного ранее словаря.
2)get_range - метод возвращает курс валют за указанные даты и разницу между ними. Принимает даты в формате yyyy-mm-dd переформатирует их в формат dd/mm/yyyy
для получения курса с http://www.cbr.ru/scripts/XML_daily.asp?date_req=your_date, также принимает символьный код валюты. Далее из XML получается курс заданной валюты
для каждой из дат, рассчитывается разница курсов относительно рубля и отдается в виде словаря.

Примеры вызова методов:
[hostname]/api/v1.0/availabeCurrency
[hostname]/api/v1.0/get_range?date_start=2001-03-02&date_end=2001-03-15&currency_symbol=EUR
