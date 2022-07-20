
def calculate_average_salary(salary_from, salary_to):
    if salary_from and salary_to:
        average_salary = (salary_from + salary_to) / 2
    elif not salary_from:
        average_salary = salary_to * 0.8
    elif not salary_to:
        average_salary = salary_from * 1.2
    return average_salary