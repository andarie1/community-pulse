from flask import Blueprint, jsonify, request
from app.schemas.question import QuestionCreate, QuestionResponse
from app.models.question import Question
import pandas as pd
from pydantic import ValidationError

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов."""
    questions = Question.query.all()
    results = [QuestionResponse.from_orm(question).dict() for question in questions]
    return jsonify(results)

@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
     """Получение деталей конкретного вопроса по его ID."""
     question = Question.query.get(id)
     if question is None:
        return jsonify({'message':"Вопрос с таким ID не найден"}), 404
     return jsonify({'message': f"Вопрос: {question.text}"}), 200


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()
    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    question = Question(text=question_data.text)
    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionResponse(id=question.id, text=question.text).dict()), 201

@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Редактирование вопроса """
    question = Question.query.get(id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'id': question.id, 'text': question.text}), 200
    return jsonify({'error': 'Missing data'}), 400



@questions_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def delete_question(id):
    """Удаление вопроса."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200



