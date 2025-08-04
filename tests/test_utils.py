from unittest.mock import Mock,patch
from src.utils import get_greating_client, get_json_with_data, get_often_operations, get_top_five, get_user_settings, get_convert, get_papirus
import datetime

def test_greating_client():
    assert get_greating_client() == 'Доброе утро'

@patch('requests.get')
def test_get_convert(mock_get):
    test_api_value = {"rates": {
            "RUB": 91.985415
        }}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = test_api_value
    list_current = ["USD", "EUR"]
    assert get_convert(list_current) == [{"currency": "USD", "rate": 91.985415}, {"currency": "EUR", "rate": 91.985415}]

@patch('requests.get')
def test_get_papirus(mock_get):
    test_api_value = {"c":523.745,"d":-9.755,"dp":-1.8285,"h":536.5,"l":523.6801,"o":536.5,"pc":533.5,"t":1754061918}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = test_api_value
    list_papirus = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    assert get_papirus(list_papirus) ==  [{"stock": "AAPL", "price": 523.745}, {"stock": "AMZN", "price": 523.745}, {"stock": "GOOGL", "price": 523.745}, {"stock": "MSFT", "price": 523.745}, {"stock": "TSLA", "price": 523.745}]


