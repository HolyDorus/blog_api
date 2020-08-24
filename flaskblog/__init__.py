# Load .env file
from dotenv import load_dotenv
load_dotenv()


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import ValidationError
from .settings import settings
from .utils import format_validation_error


app = Flask(__name__)
app.config.from_object(settings)

db = SQLAlchemy(app)


from .blueprints.articles_routes import articles_bp
from .blueprints.auth_routes import auth_bp
from .middlewares import AuthorizationMiddleware, JSONTypeOnlyMiddleware


app.register_blueprint(articles_bp)
app.register_blueprint(auth_bp)

app.wsgi_app = AuthorizationMiddleware(app.wsgi_app)
app.wsgi_app = JSONTypeOnlyMiddleware(app.wsgi_app)


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    errors = format_validation_error(e.errors())
    return jsonify(errors), 400
