
import json
import datetime
from src.views import get_main_page_info
import pandas as pd

#main_info = get_main_page_info("2021-12-11 01:02:03")
#print(main_info)
#dict_data = main_info.to_dict(orient="records")
def analysys_stonks(data_for_analys, month, year):
    need_dict = {}
    result_cachback = {}
    number = 0
    date_user = datetime.datetime(year, month, 1).strftime("%m.%Y")
    for data in data_for_analys:
        need_dict[data.get('Категория')] = 0
    for data in data_for_analys:
        if pd.isna(data.get('Кэшбэк')):
            number += 1
        else:
            if data.get('Категория') in need_dict and date_user in data.get('Дата операции')[:]:
                need_dict[data.get('Категория')] += data.get('Кэшбэк')
            elif data.get('Категория') not in need_dict and date_user in data.get('Дата операции')[:]:
                need_dict[data.get('Категория')] = data.get('Кэшбэк')

    sorted_kashback =dict(sorted(need_dict.items(), key = lambda x: x[1], reverse=True ))
    for key, value in sorted_kashback.items():
        if value != 0:
            result_cachback[key] = value
    result_cachback = json.dumps(result_cachback, ensure_ascii=False)
    return result_cachback
