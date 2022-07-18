from terminaltables import AsciiTable

from headhunter import main_hh
from superjob import main_sj


table_data = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

vacancies_statistic_sj = main_sj()
title_sj = 'SuperJob Moscow'

vacancies_statistic_hh = main_hh()
title_hh = 'Headhunter Moscow'


def create_table(vacancies_statistic, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано',
         'Средняя зарплата']]
    for language, data in vacancies_statistic.items():
        table_data.append([language] + list(data.values()))
    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == '__main__':
    create_table(vacancies_statistic_hh, title_hh)
    print()
    create_table(vacancies_statistic_sj, title_sj)
