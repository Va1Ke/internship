"""first

Revision ID: 6013a9ddf857
Revises: da061f5d07e7
Create Date: 2022-11-03 13:47:39.422201

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6013a9ddf857'
down_revision = 'da061f5d07e7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations_from_owner', sa.Column('invited_user_id', sa.Integer(), nullable=True))
    op.drop_constraint('invitations_from_owner_owner_id_fkey', 'invitations_from_owner', type_='foreignkey')
    op.create_foreign_key(None, 'invitations_from_owner', 'users', ['invited_user_id'], ['id'])
    op.drop_column('invitations_from_owner', 'owner_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invitations_from_owner', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'invitations_from_owner', type_='foreignkey')
    op.create_foreign_key('invitations_from_owner_owner_id_fkey', 'invitations_from_owner', 'users', ['owner_id'], ['id'])
    op.drop_column('invitations_from_owner', 'invited_user_id')
    # ### end Alembic commands ###
