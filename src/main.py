from src.views import get_main_page_info
from src.services import  analysys_stonks
from src.utils import get_json_with_data
from src.reports import spending_by_category
import os
def main():
    file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
    main_info = get_main_page_info("2021-12-11 01:02:03")
    print(main_info)
    dict_data = get_json_with_data(file_with_date).to_dict(orient="records")
    service_result = analysys_stonks(dict_data,6, 2021)
    print(service_result)
    report_result = spending_by_category(get_json_with_data(file_with_date),'Фастфуд','2021-04-05 11:02:03')
    print(report_result)
if __name__ == '__main__':
    main()