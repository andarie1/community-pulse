from app.models import db

#many-to-many
question_category = db.Table(
    'question_category',
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)

    responses = db.relationship('Response', backref='question', lazy='joined')
    categories = db.relationship('Category', secondary=question_category, back_populates='questions')

    def __repr__(self):
        return f'Question: {self.text}'


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    questions = db.relationship('Question', secondary=question_category, back_populates='categories')

    def __repr__(self):
        return f'Category: {self.name}'


class Statistic(db.Model):
    __tablename__ = 'statistics'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)
    agree_count = db.Column(db.Integer, nullable=False, default=0)
    disagree_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return '<Statistic for Question %r: %r agree, %r disagree>' % (self.question_id, self.agree_count, self.disagree_count)
