from pprint import pprint

import requests as requests

import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
client_id = os.getenv('ID')


languages = ['Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Shell']
sj_url = 'https://api.superjob.ru/2.0/vacancies'


def get_response(language, page, url):
    headers = {'X-Api-App-Id': secret_key}
    params = {'key': 48, 'keywords': f'Разработчик {language}', 'town': 4, 'page': page}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_all_language_vacancies(language, url):
    language_vacancies_list = []
    page = 0
    first_list_vacancies = get_response(language, page, url)
    vacancies_per_page = 20
    total_vacancies = first_list_vacancies['total']
    language_vacancies_list.extend(first_list_vacancies['objects'])
    while 0 < total_vacancies:
        vacancies = get_response(language, page, url)
        page += 1
        total_vacancies -= vacancies_per_page
        language_vacancies_list.extend(vacancies['objects'])
    return language_vacancies_list


def predict_rub_salary_for_superjob(vacancy):
    if vacancy['payment_from'] and vacancy['payment_to']:
        average_salary = (vacancy['payment_from'] + vacancy['payment_to']) / 2
    elif vacancy['payment_from'] == 0:
        average_salary = vacancy['payment_to'] * 0.8
    elif vacancy['payment_to'] == 0:
        average_salary = vacancy['payment_from'] * 1.2
    else:
        average_salary = None
    return average_salary


def get_total_average_salary(url, languages):
    sj_vacancies = {}
    for language in languages:
        sum_of_salary = 0
        count = 0
        vacancies = get_all_language_vacancies(language, url)
        # print(111, vacancies, language)
        for vacancy in vacancies:
            average_salary = predict_rub_salary_for_superjob(vacancy)
            if average_salary == 0:
                continue
            else:
                sum_of_salary += average_salary
                count += 1
        # if count == 0:

        sj_vacancies.setdefault(
            language,
            {
                "vacancies_found": len(vacancies),
                "vacancies_processed": count,
                "average_salary": int(sum_of_salary / count) if count else 0,
            },
        )
    return sj_vacancies


def main_sj():
    total_salary = get_total_average_salary(sj_url, languages)
    return total_salary


if __name__ == '__main__':
    main_sj()
