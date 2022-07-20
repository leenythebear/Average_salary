from terminaltables import AsciiTable

from headhunter import main_hh
from superjob import main_sj


def create_table(vacancies_statistic, title):
    table_headers = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language, data in vacancies_statistic.items():
        table_headers.append([language] + list(data.values()))
    table = AsciiTable(table_headers, title)
    return table.table


def main():
    sj_vacancies_statistic = main_sj()
    sj_title = "SuperJob Moscow"

    hh_vacancies_statistic = main_hh()
    hh_title = "Headhunter Moscow"

    print(create_table(hh_vacancies_statistic, hh_title))
    print()
    print(create_table(sj_vacancies_statistic, sj_title))


if __name__ == "__main__":
    main()
