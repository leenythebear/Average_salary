import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

from headhunter import get_hh_total_average_salary
from settings import LANGUAGES
from superjob import get_sj_total_average_salary


def create_table(vacancies_statistic, title):
    table_headers = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for language, vacancy_statistic in vacancies_statistic.items():
        table_headers.append([language] + list(vacancy_statistic.values()))
    table = AsciiTable(table_headers, title)
    return table.table


def main():
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    sj_vacancies_statistic = get_sj_total_average_salary(LANGUAGES, secret_key)
    sj_title = "SuperJob Moscow"

    hh_vacancies_statistic = get_hh_total_average_salary(LANGUAGES)
    hh_title = "Headhunter Moscow"

    print(create_table(hh_vacancies_statistic, hh_title))
    print()
    print(create_table(sj_vacancies_statistic, sj_title))


if __name__ == "__main__":
    main()
