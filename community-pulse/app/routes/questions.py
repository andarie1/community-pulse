from flask import Blueprint, request, jsonify
from app.models import db, Question, Category
from pydantic import ValidationError
from app.schemas.question import QuestionResponse, QuestionCreate, QuestionUpdate, CategoryResponse, CategoryCreate, CategoryUpdate

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')

# --- ЭНДПОИНТЫ ВОПРОСОВ ---

@questions_bp.route('/', methods=['GET'])
def get_questions():
    """Получение списка всех вопросов с категориями."""
    questions = Question.query.all()
    results = [QuestionResponse(
        id=q.id, text=q.text,
        category=CategoryResponse(id=q.category.id, name=q.category.name) if q.category else None
    ).model_dump() for q in questions]
    return jsonify(results)


@questions_bp.route('/', methods=['POST'])
def create_question():
    """Создание нового вопроса с возможностью указания категории."""
    data = request.get_json()
    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category.query.get(question_data.category_id) if question_data.category_id else None
    question = Question(text=question_data.text, category=category)
    db.session.add(question)
    db.session.commit()

    return jsonify(QuestionResponse(id=question.id, text=question.text,
                                    category=CategoryResponse(id=category.id, name=category.name) if category else None
                                    ).model_dump()), 201


@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    """Редактирование вопроса с возможностью изменения категории."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404

    data = request.get_json()
    try:
        question_data = QuestionUpdate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if question_data.text:
        question.text = question_data.text

    if question_data.category_id is not None:
        category = Category.query.get(question_data.category_id)
        if category is None:
            return jsonify({'error': 'Category not found'}), 404
        question.category = category

    db.session.commit()

    return jsonify(QuestionResponse(
        id=question.id,
        text=question.text,
        category=CategoryResponse(id=question.category.id, name=question.category.name) if question.category else None
    ).model_dump()), 200


@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Удаление вопроса."""
    question = Question.query.get(id)
    if question is None:
        return jsonify({'message': "Вопрос с таким ID не найден"}), 404

    db.session.delete(question)
    db.session.commit()

    return jsonify({'message': f"Вопрос с ID {id} удален"}), 200


# --- ЭНДПОИНТЫ КАТЕГОРИЙ ---

@categories_bp.route('/', methods=['POST'])
def create_category():
    """Создание новой категории."""
    data = request.get_json()
    try:
        category_data = CategoryCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category(name=category_data.name)
    db.session.add(category)
    db.session.commit()

    return jsonify(CategoryResponse(id=category.id, name=category.name).model_dump()), 201


@categories_bp.route('/', methods=['GET'])
def get_categories():
    """Получение списка всех категорий."""
    categories = Category.query.all()
    results = [CategoryResponse(id=c.id, name=c.name).model_dump() for c in categories]
    return jsonify(results)


@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    """Обновление категории по ID."""
    category = Category.query.get(id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json()
    try:
        category_data = CategoryUpdate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category.name = category_data.name
    db.session.commit()

    return jsonify(CategoryResponse(id=category.id, name=category.name).model_dump()), 200


@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Удаление категории по ID."""
    category = Category.query.get(id)
    if category is None:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': f'Category with ID {id} deleted'}), 200


