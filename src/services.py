
import json
import datetime
from src.views import get_main_page_info
import pandas as pd
import os
import logging

logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'services.log')
logger = logging.getLogger('services')
console_handler = logging.FileHandler(logs_dir,  mode='w', encoding='utf-8')
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

def analysys_stonks(data_for_analys, month, year):
    need_dict = {}
    result_cachback = {}
    number = 0
    logger.info('Форматирование даты')
    date_user = datetime.datetime(year, month, 1).strftime("%m.%Y")
    for data in data_for_analys:
        need_dict[data.get('Категория')] = 0
    logger.info('Сортировка по категориям')
    for data in data_for_analys:
        if pd.isna(data.get('Кэшбэк')):
            number += 1
        else:
            if data.get('Категория') in need_dict and date_user in data.get('Дата операции')[:]:
                need_dict[data.get('Категория')] += data.get('Кэшбэк')
            elif data.get('Категория') not in need_dict and date_user in data.get('Дата операции')[:]:
                need_dict[data.get('Категория')] = data.get('Кэшбэк')
    sorted_kashback =dict(sorted(need_dict.items(), key = lambda x: x[1], reverse=True ))
    logger.info('Сортировка по убыванию')
    for key, value in sorted_kashback.items():
        if value != 0:
            result_cachback[key] = value
    result_cachback_json = json.dumps(result_cachback, ensure_ascii=False)
    return result_cachback_json
