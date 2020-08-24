from typing import List


def count_digits_in_str(string: str) -> int:
    """Counts the number of digits in a string"""
    count = 0
    for char in string:
        if char.isdigit():
            count += 1
    return count


def count_capital_in_str(string: str) -> int:
    """Counts the number of capital letters in a string"""
    count = 0
    for char in string:
        if char.isupper():
            count += 1
    return count


def format_validation_error(errors: list) -> List[dict]:
    """Format validation errors from pydantic style"""
    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            'field': error['loc'][0],
            'message': error['msg'].capitalize()
        })
    return formatted_errors
