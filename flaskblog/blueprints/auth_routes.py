from flask import Blueprint

from .. import services


auth_bp = Blueprint('auth', __name__, url_prefix='/auth/')


@auth_bp.route('login/', methods=['POST'])
def user_login():
    return services.user_login()
