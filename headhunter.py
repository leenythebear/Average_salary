import requests as requests


hh_url = "https://api.hh.ru/vacancies"
languages = [
    "Python",
    "JavaScript",
    "Java",
    "Ruby",
    "PHP",
    "C++",
    "C#",
    "C",
    "Go",
    "Shell",
]


def get_response(language, page, hh_url):
    search = {
        "text": f"Разработчик {language}",
        "area": 1,
        "period": 30,
        "page": page,
    }
    headers = {"User-Agent": "User-Agent"}
    page_response = requests.get(hh_url, headers=headers, params=search)
    page_response.raise_for_status()
    return page_response.json()


def get_all_language_vacancies(language, hh_url):
    language_vacancies_list = []
    page = 0
    foo_bar = get_response(language, page, hh_url)
    page += 1
    pages_number = foo_bar['pages']
    while page < pages_number:
        vacancies = get_response(language, page, hh_url)
        page += 1
        language_vacancies_list.extend(vacancies['items'])
    return language_vacancies_list


def foo_bar(languages):
    vacancies_hh = {}
    for language in languages:
        sum_of_salary = 0
        count = 0
        vacancies = get_all_language_vacancies(language, hh_url)
        for vacancy in vacancies:
            average_salary = predict_rub_salary_hh(vacancy)
            if not average_salary:
                continue
            else:
                sum_of_salary += average_salary
                count += 1
        vacancies_hh.setdefault(
            language,
            {
                "vacancies_found": len(vacancies),
                "vacancies_processed": count,
                "average_salary": int(sum_of_salary / count),
            },
        )
    return vacancies_hh


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


def main_hh():
    average_salary = foo_bar(languages)
    return average_salary


if __name__ == '__main__':
    main_hh()
