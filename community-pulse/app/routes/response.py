from flask import Blueprint, request, jsonify
from app.models.response import Response
from app.models.question import Question, Statistic
from app.models import db

response_bp = Blueprint('response', __name__, url_prefix='/responses')

@response_bp.route('/', methods=['GET'])
def get_responses():
    """Получение статистики ответов."""
    data = request.get_json()
    if not data or 'question_id' not in data or not data['question_id']:
        return jsonify({"error": "Not found"}), 404

    return jsonify({"message": "Получение статистики ответов"})

@response_bp.route('/', methods=['POST'])
def add_response():
    """Добавление нового ответа на вопрос."""
    data = request.get_json()
    if not data or 'question_id' not in data or not data['question_id']:
        return jsonify({"error": "Not found"}), 404

    response = Response(
        question_id=data['question_id'],
        is_agree=data['is_agree']
    )
    db.session.add(response)
    db.session.commit()

    # Получаем статистику по question_id
    statistics = Statistic.query.get(data['question_id'])
    if not statistics:
        statistics = Statistic(
            question_id=data['question_id'],
            agree_count=0,
            disagree_count=0
        )
        db.session.add(statistics)

    # Обновляем статистику
    if data['is_agree']:
        statistics.agree_count += 1
    else:
        statistics.disagree_count += 1

    db.session.commit()

    return jsonify({'message': f'Ответ на вопрос под номером {data["question_id"]} сохранен'})
