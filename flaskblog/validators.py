from typing import List


def article_create_validate(title: str, content: str, author_id: int) -> List[str]:
    errors = []

    if not title:
        errors.append('Field \'title\' must be filled!')
    elif len(title) >= 100:
        errors.append('Field \'title\' must be less than 100 characters!')

    if not content:
        errors.append('Field \'content\' must be filled!')
    if not author_id:
        errors.append('The author of the article was not found!')

    return errors


def article_update_validate(title: str, content: str) -> List[str]:
    errors = []

    if title and len(title) >= 100:
        errors.append('Field \'title\' must be less than 100 characters!')

    return errors


def user_login_validate(username: str, password: str) -> List[str]:
    errors = []

    if not username:
        errors.append('Field \'username\' must be filled!')
    if not password:
        errors.append('Field \'password\' must be filled!')

    return errors
