
from datetime import datetime
from random import randint


age_ranges = {
        "infant": (0, 1),
        "children": (2, 11),
        "tng": (12, 14),
        "adults": (15, 120)
}


def calculate_age(day, month, year):
    today = datetime.now()
    birth = datetime(year, month, day)
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return age


def validate_age_by_type(tipo, day, month, year):
    age = calculate_age(day, month, year)
    min_age, max_age = age_ranges[tipo]
    return min_age <= age <= max_age

def generate_date_of_birth(tipo):
    today = datetime.now()
    age_min, age_max = age_ranges[tipo]
    min_year = today.year - age_max
    max_year = today.year - age_min
    min_year = max(min_year, 1907)
    year = randint(min_year, max_year)
    month = randint(1, 12)
    day = randint(1, 28)
    return day, month, year


def map_types_by_code(list_codes):
    code_to_type = {
        1: "adults",
        2: "tng",
        3: "children",
        4: "infant"
    }
    return [code_to_type[c] for c in list_codes]