from typing import Optional
from hashlib import pbkdf2_hmac

import jwt

from .settings import settings


def generate_password(password: str) -> str:
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        settings.SECRET_KEY.encode('utf-8'),
        10000
    ).hex()


def is_correct_password(password: str, hash: str) -> bool:
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        settings.SECRET_KEY.encode('utf-8'),
        10000
    ).hex() == hash


def create_acces_token(user_id: int) -> str:
    return jwt.encode({
            'user_id': user_id,
        },
        settings.SECRET_KEY,
        algorithm='HS256'
    ).decode()


def get_acces_token_from_request(request) -> Optional[str]:
    auth_data = request.headers.get('Authorization')

    if not auth_data:
        return None

    if not auth_data.startswith('Bearer '):
        return None

    return auth_data[7:]


def get_user_id_from_acces_token(token: str):
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        return data['user_id']
    except Exception:
        return None
