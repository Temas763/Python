def is_year_leap(year):
    return year % 4 == 0


year_to_check = 2024
result = is_year_leap(year_to_check)
print(f"год {year_to_check}: {result}")
