import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date


def cache():
    curr = {
        'currency': []
    }
    '''
    Получение списка валют, которые можно использовать (символьный код (RUB, EUR), название)
    '''
    d = date.today().isoformat()
    root = ET.fromstring(requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={parse_date(d)}").text)
    i=0
    for child in root:
        if child[1].text:
            curr['currency'].append({"fullName":child[3].text, "SymbolName":child[1].text})
    return curr


class SymbException(BaseException):
    pass


def currency_rate(date_req1: str, date_req2: str, val_char: str):

    '''
    Получение разницы курса относительно рубля между двумя датами
    '''
    try:
        date_req1 = parse_date(date_req1)
    except ValueError:
        return f'Invalid date {date_req1}'
    try:
        date_req2 = parse_date(date_req2)
    except ValueError:
        return f'Invalid date {date_req2}'

    curr_rate = {
    }

    root = ET.fromstring(requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req1}").text)
    for child in root:
        if child[1].text == val_char:
            curr_rate[date_req1] = child[4].text

    root = ET.fromstring(requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req2}").text)
    for child in root:
        if child[1].text == val_char:
            curr_rate[date_req2] = child[4].text

    try:
        cr1 = float(curr_rate[date_req1].replace(',', '.'))
    except KeyError:
        return f'Is not currency rate from this date {date_req1}'
    try:
        cr2 = float(curr_rate[date_req2].replace(',', '.'))
    except KeyError:
        return f'Ts not currency rate from this date {date_req2}'
    curr_rate['change'] = str(round(cr2-cr1, 5)).replace('.', ',')

    return {
        "dateStart": curr_rate[date_req1],
        "dateEnd": curr_rate[date_req2],
        "change": curr_rate['change']
    }


def parse_date(date: str):
    date = datetime.strptime(date, '%Y-%m-%d')
    date_obj = datetime.strftime(date, '%d/%m/%Y')
    return date_obj
