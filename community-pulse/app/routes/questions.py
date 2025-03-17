from flask import Blueprint, request, jsonify
from app.models import db, Question, Category
from pydantic import ValidationError
from app.schemas.question import QuestionResponse, QuestionCreate, QuestionUpdate, CategoryResponse, CategoryCreate, CategoryUpdate

qa_bp = Blueprint('qa', __name__, url_prefix='/qa')

# --- QUESTIONS ---

@qa_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get all questions with their categories."""
    questions = Question.query.all()
    return jsonify([
        QuestionResponse(
            id=q.id,
            text=q.text,
            categories=[CategoryResponse(id=c.id, name=c.name) for c in q.categories]
        ).model_dump() for q in questions
    ])


@qa_bp.route('/questions', methods=['POST'])
def create_question():
    """Create a new question with optional category."""
    data = request.get_json()
    try:
        question_data = QuestionCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    categories = Category.query.filter(
        Category.id.in_(question_data.category_ids)).all() if question_data.category_ids else []
    question = Question(text=question_data.text, categories=categories)
    db.session.add(question)
    db.session.commit()

    return jsonify(QuestionResponse(
        id=question.id, text=question.text,
        categories=[CategoryResponse(id=c.id, name=c.name) for c in question.categories]
    ).model_dump()), 201


@qa_bp.route('/questions/<int:id>', methods=['PUT'])
def update_question(id):
    """Update a question."""
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    data = request.get_json()
    try:
        question_data = QuestionUpdate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if question_data.text:
        question.text = question_data.text

    if question_data.category_ids is not None:
        question.categories = Category.query.filter(Category.id.in_(question_data.category_ids)).all()

    db.session.commit()
    return jsonify(QuestionResponse(
        id=question.id, text=question.text,
        categories=[CategoryResponse(id=c.id, name=c.name) for c in question.categories]
    ).model_dump()), 200


@qa_bp.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    """Delete a question."""
    question = Question.query.get(id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    db.session.delete(question)
    db.session.commit()
    return jsonify({'message': f'Question {id} deleted'}), 200


# --- CATEGORIES ---

@qa_bp.route('/categories', methods=['POST'])
def create_category():
    """Create a category."""
    data = request.get_json()
    try:
        category_data = CategoryCreate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category = Category(name=category_data.name)
    db.session.add(category)
    db.session.commit()
    return jsonify(CategoryResponse(id=category.id, name=category.name).model_dump()), 201


@qa_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    categories = Category.query.all()
    return jsonify([CategoryResponse(id=c.id, name=c.name).model_dump() for c in categories])


@qa_bp.route('/categories/<int:id>', methods=['PUT'])
def update_category(id):
    """Update a category."""
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    data = request.get_json()
    try:
        category_data = CategoryUpdate(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    category.name = category_data.name
    db.session.commit()
    return jsonify(CategoryResponse(id=category.id, name=category.name).model_dump()), 200


@qa_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    """Delete a category."""
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': f'Category {id} deleted'}), 200



