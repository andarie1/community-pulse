from flask import Blueprint, request, jsonify
from app.models import db, Category, Question
from app.schemas.question import CategoryCreate, CategoryResponse, CategoryUpdate

category_bp = Blueprint('categories', __name__, url_prefix='/categories')


# ------------------ CREATE CATEGORY ------------------
@category_bp.route('', methods=['POST'])
def create_category():
    data = request.json
    category_data = CategoryCreate(**data)
    category = Category(name=category_data.name)
    db.session.add(category)
    db.session.commit()
    return jsonify(CategoryResponse.from_orm(category).dict()), 201


# ------------------ READ ALL CATEGORIES ------------------
@category_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([CategoryResponse.from_orm(cat).dict() for cat in categories]), 200


# ------------------ UPDATE CATEGORY ------------------
@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    update_data = CategoryUpdate(**data)
    if update_data.name:
        category.name = update_data.name
    db.session.commit()
    return jsonify(CategoryResponse.from_orm(category).dict()), 200


# ------------------ DELETE CATEGORY ------------------
@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Категория успешно удалена.'}), 200
