
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