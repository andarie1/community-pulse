from app import create_app, db
from app.models import Question, Response, Category  # Импортируешь модели, чтобы миграции их "видели"

app = create_app()
