from app import create_app
from app.models import db, Question, Category, Response
from sqlalchemy import text
import random  # Для случайного распределения ответов

app = create_app()

with app.app_context():
    # ✅ Очищаем старые связи и данные
    db.session.execute(text('DELETE FROM question_categories;'))
    db.session.query(Response).delete()
    db.session.query(Question).delete()
    db.session.query(Category).delete()
    db.session.commit()

    # ✅ Создаем категории
    python_category = Category(name='Python')
    web_category = Category(name='Web Development')
    db_category = Category(name='Databases')

    db.session.add_all([python_category, web_category, db_category])
    db.session.commit()

    # ✅ Вопросы закрытого типа (да/нет)
    questions = [
        (['Python', 'Web Development'], 'Вы когда-либо использовали фреймворк Flask?'),
        (['Python'], 'Вы умеете создавать виртуальное окружение в Python?'),
        (['Databases'], 'Вы понимаете, как устроены реляционные базы данных?'),
        (['Python', 'Databases'], 'Вы когда-либо подключали Flask-приложение к базе данных?'),
        (['Web Development'], 'Вы умеете развернуть Flask-приложение на сервере?'),
        (['Python'], 'Вы знакомы с основами ООП в Python?'),
        (['Web Development'], 'Вы используете систему контроля версий Git?'),
        (['Web Development'], 'Вы когда-либо деплоили приложение в облако?'),
        (['Python', 'Databases'], 'Вы использовали ORM SQLAlchemy для работы с базами данных?'),
        (['Databases'], 'Вы знаете, как написать миграции базы данных с Alembic?')
    ]

    question_objects = []

    # ✅ Создаем вопросы и назначаем категории
    for cat_names, text_question in questions:
        q = Question(text=text_question)
        q.categories = [python_category if name == 'Python' else web_category if name == 'Web Development' else db_category for name in cat_names]
        question_objects.append(q)

    db.session.add_all(question_objects)
    db.session.commit()

    # ✅ Генерируем ответы для статистики (например, случайно по 5 штук на вопрос)
    responses = []
    for question in question_objects:
        for _ in range(5):  # 5 ответов на каждый вопрос
            response = Response(
                question_id=question.id,
                is_agree=random.choice([True, False])  # Случайный выбор: согласен/не согласен
            )
            responses.append(response)

    db.session.add_all(responses)
    db.session.commit()

    print("✅ База успешно заполнена вопросами, категориями и ответами для статистики!")




