import requests as requests

from settings import SJ_URL, SECRET_KEY


def get_response(language, page):
    vacancies_sphere = 48
    moscow_city_id = 4
    headers = {"X-Api-App-Id": SECRET_KEY}
    params = {
        "key": vacancies_sphere,
        "keywords": f"Разработчик {language}",
        "town": moscow_city_id,
        "page": page,
    }
    response = requests.get(SJ_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_all_language_vacancies(language):
    language_vacancies = []
    page = 0
    first_page_vacancies = get_response(language, page)
    vacancies_per_page = 20
    total_vacancies = first_page_vacancies['total']
    language_vacancies.extend(first_page_vacancies['objects'])
    while 0 < total_vacancies:
        vacancies = get_response(language, page)
        page += 1
        total_vacancies -= vacancies_per_page
        language_vacancies.extend(vacancies['objects'])
    return language_vacancies


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


def get_sj_total_average_salary(languages):
    sj_vacancies = {}
    for language in languages:
        sum_of_salary = 0
        count = 0
        vacancies = get_all_language_vacancies(language)
        for vacancy in vacancies:
            average_salary = predict_rub_salary_for_superjob(vacancy)
            if average_salary:
                sum_of_salary += average_salary
                count += 1
        sj_vacancies.setdefault(
            language,
            {
                "vacancies_found": len(vacancies),
                "vacancies_processed": count,
                "average_salary": int(sum_of_salary / count) if count else 0,
            },
        )
    return sj_vacancies


