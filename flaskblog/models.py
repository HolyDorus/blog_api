from datetime import datetime

from . import db
from .auth import generate_password


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    published_datetime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return f'<Article title={self.title}>'


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(65), nullable=False)
    email = db.Column(db.String(40), unique=True)
    articles = db.relationship(
        'Article', backref='author',
        cascade='all, delete', lazy='dynamic'
    )
    register_datetime = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.password = generate_password(password)

    def __repr__(self):
        return f'<User username={self.username}, email={self.email}>'
