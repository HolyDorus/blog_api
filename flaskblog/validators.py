from typing import Optional

from pydantic import BaseModel, validator

from .utils import count_digits_in_str, count_capital_in_str


class UserLoginValidator(BaseModel):
    username: str
    password: str


class UserValidator(BaseModel):
    username: str
    password: str
    email: str

    @validator('username')
    def username_validator(value):
        max_len = 40
        if len(value) >= max_len:
            raise ValueError(f'Must be less than {max_len} characters')
        return value

    @validator('password')
    def password_validator(value):
        min_len = 8
        if len(value) < min_len:
            raise ValueError(f'Must be at least {min_len} characters')

        min_digits = 2
        if count_digits_in_str(value) < min_digits:
            raise ValueError(
                f'Must be at least {min_digits} digits in password'
            )

        min_capital = 1
        if count_capital_in_str(value) < min_capital:
            raise ValueError(
                f'Must be at least {min_capital} capital letters in password'
            )

        return value


class ArticleValidator(BaseModel):
    title: str
    content: str

    @validator('title')
    def title_validator(value):
        max_len = 100
        if len(value) > max_len:
            raise ValueError(
                f'The length must not exceed {max_len} characters'
            )
        return value


class ArticleUpdateValidator(BaseModel):
    title: Optional[str]
    content: Optional[str]

    @validator('title')
    def title_validator(value):
        max_len = 100
        if len(value) > max_len:
            raise ValueError(
                f'The length must not exceed {max_len} characters'
            )
        return value
