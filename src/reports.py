import pandas as pd
import datetime
import os
from functools import wraps
import logging
from typing import Optional

logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'reports.log')
logger = logging.getLogger('reports')
console_handler = logging.FileHandler(logs_dir,  mode='w', encoding='utf-8')
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
print(file_with_date)


def report_to_file(filename: str):
    """Декоратор для функций-отчетов, который записывает в файл результат
    """
    logger.info('Запись отчёта')

    def wrapper(func_category):
        @wraps(func_category)
        def inner(*args, **kwargs):
            result = None
            if filename:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(f"{func_category(*args, **kwargs)}")
            else:
                with open('user_category.json', 'a', encoding='utf-8') as file:
                    file.write(f'{func_category(*args, **kwargs)}')
            return result
        return inner
    return wrapper


@report_to_file('user_category.json')
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str]=None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца
    """
    logger.info('Составление отчёта по категории и дате')
    if date is None:
        date_dt = datetime.datetime.now().replace(microsecond=0)
    else:
        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_dt = date_dt - pd.DateOffset(months=3)
    selected_spendings = transactions[(pd.to_datetime(transactions['Дата операции'], dayfirst=True) >= start_dt)
                                      & (pd.to_datetime(transactions['Дата операции'], dayfirst=True) <= date_dt)
                                      & (transactions['Категория'] == category) & (transactions['Сумма операции'] < 0)]
    return selected_spendings
