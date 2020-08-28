import datetime

from flask import Blueprint, jsonify

from .. import services
from ..validators import UserLoginValidator, UserRegisterValidator
from .. import auth
from ..decorators import json_object_required
from ..serializers import UserSerializer


auth_bp = Blueprint('auth', __name__, url_prefix='/auth/')


@auth_bp.route('login/', methods=['POST'])
@json_object_required
def login_user(data: dict):
    """Authorizes the user and returns access and refresh tokens"""
    validated_data = UserLoginValidator(**data)

    user = services.get_user_by_username(validated_data.username)

    if not user:
        return jsonify(
            {'errors': ['No user with this username was found']}
        ), 404

    if not auth.is_correct_password(validated_data.password, user.password):
        return jsonify({'errors': ['Invalid password']}), 400

    exp_at = datetime.datetime.utcnow() + datetime.timedelta(hours=5)
    access_token = auth.create_token(user.id, exp_at)
    refresh_token = auth.create_token(user.id)

    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token
    })


@auth_bp.route('register/', methods=['POST'])
@json_object_required
def register_user(data: dict):
    """Registers a new user"""
    validated_data = UserRegisterValidator(**data)

    user = services.get_user_by_username(validated_data.username)

    if user:
        return jsonify(
            {'errors': ['A user with the same name already exists']}
        ), 400

    user = services.get_user_by_email(validated_data.email)

    if user:
        return jsonify(
            {'errors': ['A user with the same email already exists']}
        ), 400

    user = services.create_user(validated_data.dict())
    serializer = UserSerializer()

    return jsonify(serializer.serialize(user)), 201
