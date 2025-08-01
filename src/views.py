import json
import os.path
import datetime
import requests
import pandas as pd
from src.utils import get_greating_client, get_json_with_data, get_often_operations, get_top_five, get_user_settings, get_convert, get_papirus

file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
def get_main_page_info(date):
    greatings = get_greating_client(date)
    all_transactions = get_json_with_data(file_with_date)
    end_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_period = end_period.replace(day=1, hour=0, minute=0, second=0)
    selected_transactions = all_transactions[(pd.to_datetime(all_transactions['Дата операции'], dayfirst=True) >= start_period) & (pd.to_datetime(all_transactions['Дата операции'], dayfirst=True) <= end_period)]
    card_info = get_often_operations(selected_transactions)
    top_five = get_top_five(selected_transactions)
    user_json_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_settings.json')
    stock_currencies = get_user_settings(user_json_date)
    stocks = stock_currencies['user_stocks']
    currencies = stock_currencies['user_currencies']
    user_currencies = get_convert(currencies)
    user_stocks = get_papirus(stocks)
    result = {
        "greating": greatings,
        "cards": card_info,
        "top_transactions": top_five,
        "currency_rates": user_currencies,
        "stock_prices": user_stocks
    }
    return result



