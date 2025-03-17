from app import create_app
from app.models import db, Question, Response

app = create_app()

with app.app_context():
    # Удаляем старые данные
    Response.query.delete()
    Question.query.delete()
    db.session.commit()

    # Добавляем вопросы
    questions = [
        Question(text="Вы когда-нибудь использовали систему контроля версий Git?"),
        Question(text="Вы знакомы с понятием контейнеризации и развертывания приложений?"),
        Question(text="Вы знаете основы ООП в Python?"),
        Question(text="Вы пробовали разрабатывать REST API?"),
        Question(text="Вы знакомы с основами баз данных SQL?"),
    ]
    db.session.add_all(questions)
    db.session.commit()  # Фиксируем, чтобы появились ID

    # Добавляем ответы (исходя из ID вопросов)
    responses = [
        Response(question_id=questions[0].id, is_agree=True),
        Response(question_id=questions[0].id, is_agree=False),
        Response(question_id=questions[1].id, is_agree=True),
        Response(question_id=questions[1].id, is_agree=True),
        Response(question_id=questions[2].id, is_agree=False),
        Response(question_id=questions[2].id, is_agree=False),
        Response(question_id=questions[3].id, is_agree=True),
        Response(question_id=questions[3].id, is_agree=False),
        Response(question_id=questions[4].id, is_agree=True),
        Response(question_id=questions[4].id, is_agree=True),
    ]
    db.session.add_all(responses)
    db.session.commit()

    print("База данных успешно заполнена начальными данными!")

