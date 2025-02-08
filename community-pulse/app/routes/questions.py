from flask import Blueprint, jsonify, request

from app.models.question import Question
import pandas as pd

questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

@questions_bp.route('/', methods=['GET'])
def get_question():
    questions = Question.query.all()
    questions_data = [{'id': q.id, 'text': q.text} for q in questions]
    # print(questions_data)
    # print(jsonify(questions_data))
    return jsonify(questions_data)


@questions_bp.route('/', methods=['POST'])
def create_question():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({'error': 'Missing question text'}), 400

    #экземпляр класса
    question = Question(text=data['text'])
    db.session.add(question)
    db.session.commit()
    return jsonify({'id': question.id, 'text': question.text}), 201

@questions_bp.route('/questions/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404

    data = request.get_json()
    if 'text' in data:
        question.text = data['text']
        db.session.commit()
        return jsonify({'id': question.id, 'text': question.text}), 200
    return jsonify({'error': 'Missing data'}), 400



@questions_bp.route('/questions/<int:id>', methods=['GET', 'DELETE'])
def delete_question(id):
    question = Question.query.get_or_404(id)
    question.delete()
    return jsonify({'message': 'Question deleted'}), 200



