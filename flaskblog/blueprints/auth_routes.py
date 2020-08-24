from flask import Blueprint, jsonify

from .. import services
from ..validators import UserLoginValidator
from .. import auth
from ..decorators import json_object_required


auth_bp = Blueprint('auth', __name__, url_prefix='/auth/')


@auth_bp.route('login/', methods=['POST'])
@json_object_required
def user_login(data: dict):
    validated_data = UserLoginValidator(**data)

    user = services.get_user_by_username(validated_data.username)

    if not user:
        return jsonify(
            {'errors': ['No user with this username was found!']}
        ), 404

    if not auth.is_correct_password(validated_data.password, user.password):
        return jsonify({'errors': ['Invalid password!']}), 400

    return jsonify({'access_token': auth.create_acces_token(user.id)})
