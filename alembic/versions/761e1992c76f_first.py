"""first

Revision ID: 761e1992c76f
Revises: 
Create Date: 2022-11-04 13:10:47.540968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761e1992c76f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizzes', sa.Column('frequency_of_passage', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('quizzes', 'frequency_of_passage')
    # ### end Alembic commands ###