from typing import Union

from .models import Article, User


class Serializer:
    def serialize_one(self, obj):
        pass

    def serialize(self, obj) -> Union[dict, list]:
        if isinstance(obj, list):
            return [self.serialize_one(item) for item in obj]
        else:
            return self.serialize_one(obj)


class ArticleSerializer(Serializer):
    def serialize_one(self, article: Article) -> dict:
        return {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author_id,
            'published_datetime': article.published_datetime
        }


class UserSerializer(Serializer):
    def serialize_one(self, user: User) -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'register_datetime': user.register_datetime
        }
