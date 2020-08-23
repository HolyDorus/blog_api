from flask import Blueprint

from ..decorators import login_required, author_of_article_required
from .. import services


articles_bp = Blueprint('articles', __name__, url_prefix='/articles/')


@articles_bp.route('', methods=['GET'])
def get_all_articles():
    return services.get_all_articles()


@articles_bp.route('', methods=['POST'])
@login_required
def create_article():
    return services.create_article()


@articles_bp.route('<int:article_id>/', methods=['GET'])
def get_article(article_id):
    return services.get_article(article_id)


@articles_bp.route('<int:article_id>/', methods=['PATCH'])
@author_of_article_required
def update_article(article_id):
    return services.update_article(article_id)


@articles_bp.route('<int:article_id>/', methods=['DELETE'])
@author_of_article_required
def delete_article(article_id):
    return services.delete_article(article_id)
