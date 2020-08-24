from functools import wraps

from flask import request, jsonify


def json_object_required(func):
    """Available JSON body object only"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify(
                {'errors': ['Invalid data format (must be an object)']}
            ), 400
        return func(data, *args, **kwargs)
    return decorated_function


def login_required(func):
    """Available to authorized users only"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.environ.get('user'):
            return jsonify({'errors': ['Authorization required']}), 401

        return func(*args, **kwargs)
    return decorated_function


def author_of_article_required(func):
    """Available only to the author of the article"""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = request.environ.get('user')
        if not user:
            return jsonify({'errors': ['Authorization required']}), 401

        article_id = kwargs.get('article_id')
        if article_id:
            article = user.articles.filter_by(id=article_id).first()
            if not article:
                return jsonify(
                    {'errors': ['You must be the author of the article']}
                ), 400

        return func(*args, **kwargs)
    return decorated_function
