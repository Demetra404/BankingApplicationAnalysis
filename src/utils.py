import os
import datetime
import requests
import pandas as pd
import json
import logging

logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'utils.log')
logger = logging.getLogger('utils')
console_handler = logging.FileHandler(logs_dir,  mode='w', encoding='utf-8')
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def get_greating_client():
    """Функция выводит приветствие в зависимости от времени
    """
    logger.info('Приветствие')
    need_dict = {}
    new_date = datetime.datetime.now().replace(microsecond=0).strftime("%H")
    hello_message = ""
    if 0 <= int(new_date) <= 5:
        hello_message = "Доброй ночи"
    elif 6 <= int(new_date) <= 11:
        hello_message = "Доброе утро"
    elif 12 <= int(new_date) <= 17:
        hello_message = "Добрый день"
    elif 18 <= int(new_date) <= 24:
        hello_message = "Добрый вечер"
    need_dict['greeting'] = hello_message
    return hello_message


def get_json_with_data(path_to_file):
    """Функция для чтения файлов
    """
    logger.info('Чтение excel файла')
    ex_data = pd.read_excel(path_to_file)
    return ex_data


def get_often_operations(data):
    """Операции по каждой карте
    """
    logger.info('Вычисление самых частых операций')
    data_ex = data.to_dict(orient="records")
    need_list = []
    list_with_operations = []
    numberd = 0
    for data in data_ex:
        if pd.isna(data.get('Номер карты')):
            numberd += 1
        elif data.get('Номер карты') not in need_list:
            need_list.append(data.get('Номер карты'))
    i = 0
    while i <= len(need_list) - 1:
        need_dict_l = {}
        njh = 0
        klmv = 0
        for data in data_ex:
            if data.get('Номер карты') == need_list[i]:
                klmv += data.get('Сумма операции')
                if pd.isna(data.get('Кэшбэк')):
                    numberd += 1
                elif data.get('Номер карты') == need_list[i]:
                    njh += data.get('Кэшбэк')
        need_dict_l['last_digit'] = need_list[i]
        need_dict_l['total_spent'] = klmv
        need_dict_l['cashback'] = njh
        list_with_operations.append(need_dict_l)
        #groupby + агрегация
        i += 1
    return list_with_operations


def get_top_five(data):
    """Функция выдаёт топ пять операций
    """
    logger.info('Вычисление топ пяти операций')
    i = 0
    while i < 5:
        i += 1
    list_top_five = []
    ex_data = data
    data_sort = ex_data[['Сумма платежа', 'Дата платежа', 'Категория', 'Описание']].sort_values('Сумма платежа')
    top_data = data_sort.head(5)
    top_five_date = top_data.to_dict(orient="records")
    for date in top_five_date:
        dict_five = {}
        dict_five["date"] = date.get('Дата платежа')
        dict_five["amount"] = date.get('Сумма платежа')
        dict_five["category"] = date.get('Категория')
        dict_five["description"] = date.get('Описание')
        list_top_five.append(dict_five)
    #отсортировать по колонке сумма операции и вывести 5 штук
    return list_top_five


def get_convert(transactions):
    """Функция выдаёт заданный курс валют
    """
    api_currency = os.getenv('API_KEY_CURRENCY')
    logger.info('Вычисление курса валют')
    url = "https://api.apilayer.com/exchangerates_data/latest"
    list_params = transactions
    currency_list = []
    for param in list_params:
        currency_dict = {}
        params = {
            "base": param,
            "symbols": "RUB"
        }
        headers = {
            "apikey": api_currency
        }
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        currency_dict['currency'] = param
        currency_dict['rate'] = result["rates"]['RUB']
        currency_list.append(currency_dict)
    return currency_list


def get_papirus(transactions):
    """Функция выдаёт курс заданных бумаг
    """
    logger.info('Вычисление курса акций')
    list_papirus = []
    api_stocks = os.getenv('API_KEY_STOCKS')
    list_params = transactions
    for param in list_params:
        papirus_dict = {}
        url = f"https://finnhub.io/api/v1/quote?symbol={param}&token={api_stocks}"
        response = requests.get(url)
        data = response.json()
        last_price = data["c"]
        papirus_dict['stock'] = param
        papirus_dict['price'] = last_price
        list_papirus.append(papirus_dict)
    return list_papirus


def get_user_settings(path_on_user):
    """Функция считывает пользовательский файл
    """
    logger.info('Чтение пользовательский настроек')
    with open(path_on_user, 'r', encoding='utf-8') as file:
        user_json = json.load(file)
        return user_json
