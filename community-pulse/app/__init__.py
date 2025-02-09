from flask import Flask
from app.routes.questions import questions_bp, categories_bp
from app.routes.response import response_bp
from config import DevelopmentConfig
from app.models import db
from flask_migrate import Migrate

def create_app():
     app = Flask(__name__)
     app.config.from_object(DevelopmentConfig)
     app.register_blueprint(questions_bp)
     app.register_blueprint(response_bp)
     app.register_blueprint(categories_bp)
     db.init_app(app)
     migrate = Migrate()
     migrate.init_app(app, db)
     return app