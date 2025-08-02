from src.reports import spending_by_category
from src.utils import get_json_with_data
import os
import pandas as pd
def test_spending_by_category():
    file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
    for_example = spending_by_category(get_json_with_data(file_with_date), 'Фастфуд', '2021-03-04 05:06:07')
    assert for_example == None