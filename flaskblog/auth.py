from typing import Optional
from hashlib import pbkdf2_hmac

import jwt

from .settings import settings


def generate_password(password: str) -> str:
    """Creates a hashed password from a raw password"""
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        settings.SECRET_KEY.encode('utf-8'),
        10000
    ).hex()


def is_correct_password(password: str, hash: str) -> bool:
    """Compares the raw password with a hashed password"""
    return pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        settings.SECRET_KEY.encode('utf-8'),
        10000
    ).hex() == hash


def create_token(user_id: int, exp: Optional[int] = None) -> str:
    """Creates and returns a JWT with the required data"""
    data = {'user_id': user_id}

    if exp:
        data['exp'] = exp

    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm='HS256'
    ).decode()


def get_acces_token_from_request(request) -> Optional[str]:
    """Retrieves and returns a token from the request header"""
    auth_data = request.headers.get('Authorization')

    if not auth_data:
        return None

    if not auth_data.startswith('Bearer '):
        return None

    return auth_data[7:]


def get_user_id_from_acces_token(token: str) -> Optional[int]:
    """Retrieves and returns user_id from token"""
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
        return data['user_id']
    except Exception:
        return None
