"""
Type hinting example.
"""

def normalize_date(date_str: str, year: str = '2020') -> str:
    normalized_date: str = date_str + '/' + year
    return normalized_date

max: int = 100
date: str = '03/14'
new_date: str = normalize_date('03/14', '2021')
print(date + ' after normalizing is ' + new_date)
