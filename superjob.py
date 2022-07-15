from pprint import pprint

import requests as requests

import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
client_id = os.getenv('ID')


languages = ['Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Shell']
sj_url = 'https://api.superjob.ru/2.0/vacancies'


def get_vacancies_sj(language):
    headers = {'X-Api-App-Id': secret_key}
    params = {'key': 48, 'keywords': f'Разработчик {language}', 'town': 4}
    page = 0
    pages_number = 1
    response = requests.get(sj_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


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



if __name__ == '__main__':
    for language in languages:
        vacancies = get_vacancies_sj(language)
        for vacancy in vacancies['objects']:
            print(predict_rub_salary_for_superjob(vacancy))