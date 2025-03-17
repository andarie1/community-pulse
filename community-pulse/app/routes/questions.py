from flask import Blueprint, request, jsonify
from app.models import db, Question, Category, Response
from app.schemas.question import QuestionResponse, QuestionCreate, QuestionUpdate, CategoryResponse, CategoryCreate, \
    CategoryUpdate

qa_bp = Blueprint('questions', __name__, url_prefix='/questions')


# ------------------ CREATE QUESTION ------------------
@qa_bp.route('', methods=['POST'])
def create_question():
    data = request.json
    question_data = QuestionCreate(**data)
    question = Question(text=question_data.text)

    # Связываем категории
    if question_data.category_ids:
        categories = Category.query.filter(Category.id.in_(question_data.category_ids)).all()
        question.categories = categories

    db.session.add(question)
    db.session.commit()
    return jsonify(QuestionResponse.from_orm(question).dict()), 201


# ------------------ GET ALL QUESTIONS ------------------
@qa_bp.route('', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([QuestionResponse.from_orm(q).dict() for q in questions]), 200


# ------------------ UPDATE QUESTION ------------------
@qa_bp.route('/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.json
    update_data = QuestionUpdate(**data)

    if update_data.text:
        question.text = update_data.text

    if update_data.category_ids is not None:
        categories = Category.query.filter(Category.id.in_(update_data.category_ids)).all()
        question.categories = categories

    db.session.commit()
    return jsonify(QuestionResponse.from_orm(question).dict()), 200


# ------------------ DELETE QUESTION ------------------
@qa_bp.route('/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': 'Вопрос успешно удален.'}), 200


# ------------------ ALL STATISTICS ------------------
@qa_bp.route('/stats', methods=['GET'])
def get_question_stats():
    questions = Question.query.all()
    result = []

    for question in questions:
        agree_count = Response.query.filter_by(question_id=question.id, is_agree=True).count()
        disagree_count = Response.query.filter_by(question_id=question.id, is_agree=False).count()

        result.append({
            "id": question.id,
            "text": question.text,
            "agree_count": agree_count,
            "disagree_count": disagree_count
        })

    return jsonify(result), 200








