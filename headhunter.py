import requests as requests

from settings import HH_URL


def get_response(language, page):
    moscow_city_id = 1
    publication_period = 30
    search = {
        "text": f"Разработчик {language}",
        "area": moscow_city_id,
        "period": publication_period,
        "page": page,
    }
    headers = {"User-Agent": "User-Agent"}
    page_response = requests.get(HH_URL, headers=headers, params=search)
    page_response.raise_for_status()
    return page_response.json()


def get_all_language_vacancies(language):
    language_vacancies = []
    page = 0
    first_page_vacancies = get_response(language, page)
    page += 1
    language_vacancies.extend(first_page_vacancies['items'])
    pages_number = first_page_vacancies['pages']
    while page < pages_number:
        vacancies = get_response(language, page)
        page += 1
        language_vacancies.extend(vacancies['items'])
    return language_vacancies


def get_hh_total_average_salary(languages):
    hh_vacancies = {}
    for language in languages:
        sum_of_salary = 0
        count = 0
        vacancies = get_all_language_vacancies(language)
        for vacancy in vacancies:
            average_salary = predict_rub_salary_hh(vacancy)
            if not average_salary:
                continue
            else:
                sum_of_salary += average_salary
                count += 1
        hh_vacancies.setdefault(
            language,
            {
                "vacancies_found": len(vacancies),
                "vacancies_processed": count,
                "average_salary": int(sum_of_salary / count) if count else 0,
            },
        )
    return hh_vacancies


def predict_rub_salary_hh(vacancy):
    salary = vacancy["salary"]
    if not salary:
        average_salary = None
    elif not salary["currency"]:
        average_salary = None
    elif salary["currency"] != "RUR":
        average_salary = None
    elif not salary["to"]:
        average_salary = salary["from"] * 1.2
    elif not salary["from"]:
        average_salary = salary["to"] * 0.8
    else:
        average_salary = (salary["from"] + salary["to"]) / 2
    return average_salary


