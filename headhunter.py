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


def get_all_vacancies(language):
    vacancies_hh = {}
    for language in languages:
        sum_of_salary = 0
        count = 0
        page = 0
        pages_number = 1
        search = {
            "text": f"Разработчик {language}",
            "area": 1,
            "period": 30,
            "page": page,
        }
        vacancies_list = []
        while page < pages_number:
            headers = {"User-Agent": "User-Agent"}
            page_response = requests.get(hh_url, headers=headers, params=search)
            page_response.raise_for_status()
            pages_number = page_response.json()["pages"]
            page += 1
            vacancies_list.append(page_response.json())
        return vacancies_list

    #     for vacancy in page_response.json()["items"]:
    #         average_salary = predict_rub_salary_hh(vacancy)
    #         if not average_salary:
    #             continue
    #         else:
    #             sum_of_salary += average_salary
    #             count += 1
    # vacancies_hh.setdefault(
    #     language,
    #     {
    #         "vacancies_found": page_response.json()["found"],
    #         "vacancies_processed": count,
    #         "average_salary": int(sum_of_salary / count),
    #     },
    # )


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


if __name__ == '__main__':
    for language in languages:
        vacancies = get_all_vacancies(language)