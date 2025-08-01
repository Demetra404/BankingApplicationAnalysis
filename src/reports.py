import pandas as pd
import json
import datetime
import os
from functools import wraps

from pandas.core.computation.common import result_type_many

file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
print(file_with_date)

def report_to_file(filename):
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
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date= None) -> pd.DataFrame:
    if date == None:
        date_dt = datetime.datetime.now().replace(microsecond=0)
    else:
        date_dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_dt = date_dt - pd.DateOffset(months=3)
    selected_spendings = transactions[(pd.to_datetime(transactions['Дата операции'], dayfirst=True) >= start_dt) & (pd.to_datetime(transactions['Дата операции'],dayfirst=True ) <= date_dt) & (transactions['Категория'] == category ) & (transactions['Сумма операции'] < 0)]
    return selected_spendings
#print(spending_by_category(get_jsondict_with_data(file_with_date),'Фастфуд','2021-04-05 11:02:03'))