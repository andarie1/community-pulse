from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes.category import category_bp
from app.routes.questions import qa_bp
from app.routes.response import response_bp
from config import DevelopmentConfig

# Инициализация миграций вне функции, чтобы использовать из migrate.py
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(qa_bp) #questions
    app.register_blueprint(response_bp)
    app.register_blueprint(category_bp)

    return app
