from flask import request, jsonify

from . import db
from .models import Article, User
from .serializers import ArticleSerializer
from .auth import is_correct_password, create_acces_token
from . import validators


def get_all_articles():
    articles = Article.query.all()
    return jsonify(ArticleSerializer().serialize(articles))


def create_article():
    title = request.json.get('title')
    content = request.json.get('content')
    author = request.environ.get('user')

    if not author:
        return {'errors': ['Author required!']}, 401

    errors = validators.article_create_validate(
        title=title, content=content, author_id=author.id
    )

    if errors:
        return {'errors': errors}, 400

    article = Article(
        author_id=author.id,
        title=title,
        content=content
    )

    db.session.add(article)
    db.session.commit()

    return ArticleSerializer().serialize(article), 201


def get_article(article_id):
    article = Article.query.get(article_id)

    if not article:
        return {'errors': ['Article not found!']}, 404

    return ArticleSerializer().serialize(article)


def update_article(article_id):
    article = Article.query.get(article_id)

    if not article:
        return {'errors': ['Article not found!']}, 404

    title = request.json.get('title')
    content = request.json.get('content')

    errors = validators.article_update_validate(
        title=title, content=content
    )

    if errors:
        return {'errors': errors}, 400

    if title:
        article.title = title
    if content:
        article.content = content

    db.session.commit()

    return ArticleSerializer().serialize(article)


def delete_article(article_id):
    article = Article.query.get(article_id)

    if not article:
        return {'errors': ['Article not found!']}, 404

    db.session.delete(article)
    db.session.commit()

    return {'message': 'Article has been deleted'}


def user_login():
    username = request.json.get('username')
    password = request.json.get('password')

    errors = validators.user_login_validate(
        username=username, password=password
    )

    if errors:
        return {'errors': errors}, 400

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'errors': ['No user with this username was found!']}, 404

    if not is_correct_password(password, user.password):
        return {'errors': ['Invalid password!']}, 400

    return {'access_token': create_acces_token(user.id)}
