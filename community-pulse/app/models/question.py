from app.models import db


question_categories = db.Table(
    'question_categories',
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    categories = db.relationship('Category', secondary=question_categories, back_populates='questions')

    responses = db.relationship('Response', backref='question', lazy='joined')

    def __repr__(self):
        return f'Question: {self.text}'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    questions = db.relationship('Question', secondary=question_categories, back_populates='categories')

    def __repr__(self):
        return f'Category: {self.name}'
