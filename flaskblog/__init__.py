# Load .env file
from dotenv import load_dotenv
load_dotenv()


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .settings import settings


app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)


from .blueprints.articles_routes import articles_bp
from .blueprints.auth_routes import auth_bp


app.register_blueprint(articles_bp)
app.register_blueprint(auth_bp)


from .middlewares import AuthorizationMiddleware, JSONBodyOnlyMiddleware


app.wsgi_app = AuthorizationMiddleware(app.wsgi_app)
app.wsgi_app = JSONBodyOnlyMiddleware(app.wsgi_app)
