from flask import Blueprint, request, jsonify

from ..decorators import (
    login_required, author_of_article_required, json_dict_required
)
from .. import services
from ..validators import ArticleValidator, ArticleUpdateValidator
from ..serializers import ArticleSerializer


articles_bp = Blueprint('articles', __name__, url_prefix='/articles/')


@articles_bp.route('', methods=['GET'])
def get_all_articles():
    """Returns a list of articles"""
    articles = services.get_all_articles()
    serializer = ArticleSerializer()

    return jsonify(serializer.serialize(articles))


@articles_bp.route('<int:article_id>/', methods=['GET'])
def get_article(article_id: int):
    """Returns article by id"""
    article = services.get_article_by_id(article_id)

    if not article:
        return jsonify({'errors': ['Article not found!']}), 404

    serializer = ArticleSerializer()

    return jsonify(serializer.serialize(article))


@articles_bp.route('', methods=['POST'])
@json_dict_required
@login_required
def create_article(data: dict):
    """Creates an article authored by the current user and returns this
    article
    """
    validated_data = ArticleValidator(**data)

    user = request.environ['user']

    article = services.create_article_for_user(user, validated_data.dict())
    serializer = ArticleSerializer()

    return jsonify(serializer.serialize(article)), 201


@articles_bp.route('<int:article_id>/', methods=['PUT', 'PATCH'])
@json_dict_required
@author_of_article_required
def update_article(data: dict, article_id: int):
    """Updates the article by id"""
    validated_data = ArticleUpdateValidator(**data)

    article = services.update_article_if_exists(
        article_id, validated_data.dict()
    )

    if not article:
        return jsonify({'errors': ['Article not found!']}), 404

    serializer = ArticleSerializer()

    return jsonify(serializer.serialize(article))


@articles_bp.route('<int:article_id>/', methods=['DELETE'])
@author_of_article_required
def delete_article(article_id: int):
    """Removes the article by id"""
    article = services.get_article_by_id(article_id)

    if not article:
        return jsonify({'errors': ['Article not found!']}), 404

    services.delete_article(article)

    return jsonify({'message': 'Article has been deleted'})
