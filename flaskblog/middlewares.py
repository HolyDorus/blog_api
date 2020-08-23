from werkzeug.wrappers import Request, Response
import json

from .auth import get_acces_token_from_request, get_user_id_from_acces_token
from .models import User


class JSONBodyOnlyMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        if not request.data:
            return self.app(environ, start_response)

        if request.mimetype == 'application/json':
            return self.app(environ, start_response)

        response_message = {
            'errors': [
                'A The request must only be of type \'application/json\''
            ]
        }
        res = Response(
            json.dumps(response_message),
            mimetype='application/json',
            status=400
        )
        return res(environ, start_response)
        return self.app(environ, start_response)


class AuthorizationMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        token = get_acces_token_from_request(request)

        if not token:
            return self.app(environ, start_response)

        user_id = get_user_id_from_acces_token(token)

        if not user_id:
            return self.app(environ, start_response)

        user = User.query.get(user_id)

        if user:
            environ['user'] = user

        return self.app(environ, start_response)
