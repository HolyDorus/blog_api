from functools import wraps

from flask import request


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.environ.get('user'):
            return {'errors': ['Authorization required!']}, 401

        return func(*args, **kwargs)
    return decorated_function


def author_of_article_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user = request.environ.get('user')
        if not user:
            return {'errors': ['Authorization required!']}, 401

        article_id = kwargs.get('article_id')
        if article_id:
            article = user.articles.filter_by(id=article_id).first()
            if not article:
                return {'errors': ['You must be the author of the article!']}, 400

        return func(*args, **kwargs)
    return decorated_function
