"""New update

Revision ID: 14d81c3d9823
Revises: 0a0c0679e50f
Create Date: 2025-02-07 11:07:42.659347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d81c3d9823'
down_revision = '0a0c0679e50f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_category',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('question_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_category')
    # ### end Alembic commands ###
