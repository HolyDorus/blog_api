from typing import List, Optional

from . import db
from .models import Article, User


def get_all_articles() -> List[Article]:
    """Gets and returns all articles from the DB"""
    articles = Article.query.all()
    return articles


def get_article_by_id(article_id: int) -> Optional[Article]:
    """Gets and returns an article by id from the DB"""
    article = Article.query.get(article_id)
    return article


def create_article_for_user(user: User, data: dict) -> Article:
    """Creates an article with the author and writes it to the DB"""
    article = Article(**data)

    user.articles.append(article)
    db.session.commit()

    return article


def update_article_if_exists(article_id: int, data: dict) -> Optional[Article]:
    """Updates the article, if exists, and writes changes to the DB"""
    article = get_article_by_id(article_id)

    if article:
        update_article(article, data)

    return article


def update_article(article: Article, data: dict) -> None:
    """Updates the article and writes changes to the DB"""
    for key, value in data.items():
        setattr(article, key, value)

    db.session.commit()


def delete_article(article: Article) -> None:
    """Removes an article from the DB"""
    db.session.delete(article)
    db.session.commit()


def ban_article(article: Article) -> None:
    """Bans the selected article"""
    article.is_banned = True
    db.session.commit()


def unban_article(article: Article) -> None:
    """Unbans the selected article"""
    article.is_banned = False
    db.session.commit()


def get_user_by_username(username: str) -> Optional[User]:
    """Gets user by username from DB"""
    return User.query.filter_by(username=username).first()
