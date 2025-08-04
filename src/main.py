from src.views import get_main_page_info
from src.services import analysys_stonks
from src.utils import get_json_with_data
from src.reports import spending_by_category
import os
import logging

logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'main.log')
logger = logging.getLogger('main')
console_handler = logging.FileHandler(logs_dir,  mode='w', encoding='utf-8')
console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def main():
    """Основная логика программы
    """
    logger.info('Форматирование пути к файлу')
    file_with_date = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'operations.xlsx')
    logger.info('Форматирование JSONA по запросам пользователя')
    main_info = get_main_page_info("2021-12-11 01:02:03")
    print(main_info)
    dict_data = get_json_with_data(file_with_date).to_dict(orient="records")
    logger.info('Вызов сервиса')
    service_result = analysys_stonks(dict_data, 6, 2021)
    print(service_result)
    logger.info('Создание отчёта')
    report_result = spending_by_category(get_json_with_data(file_with_date), 'Фастфуд', '2021-04-05 11:02:03')
    print(report_result)


if __name__ == '__main__':
    main()
