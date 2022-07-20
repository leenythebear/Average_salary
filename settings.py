import os

from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

LANGUAGES = ['Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go', 'Shell']

SJ_URL = 'https://api.superjob.ru/2.0/vacancies'
HH_URL = "https://api.hh.ru/vacancies"
