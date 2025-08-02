from src.views import get_main_page_info


def test_get_main_page_info():
    data_test = get_main_page_info('2021-05-02 17:30:20')
    assert 'greating' in data_test
    assert 'cards' in data_test
    assert 'top_transactions' in data_test
    assert 'currency_rates' in data_test
    assert 'stock_prices' in data_test
