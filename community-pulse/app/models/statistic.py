from app.models import db


class Statistic(db.Model):
    __tablename__ = 'statistics'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    agree_count = db.Column(db.Integer, default=0, nullable=False)
    disagree_count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Statistic question_id={self.question_id} agree={self.agree_count} disagree={self.disagree_count}>"
