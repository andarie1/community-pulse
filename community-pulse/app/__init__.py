from flask import Flask
from flask_migrate import Migrate
from app.models import db
from app.routes.questions import qa_bp
from app.routes.response import response_bp
from config import DevelopmentConfig

# Инициализация миграций вне функции, чтобы использовать из migrate.py
migrate = Migrate()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Инициализация базы данных
    db.init_app(app)

    # Инициализация миграций
    migrate.init_app(app, db)

    # Регистрация Blueprint'ов
    app.register_blueprint(qa_bp)
    app.register_blueprint(response_bp)

    return app
