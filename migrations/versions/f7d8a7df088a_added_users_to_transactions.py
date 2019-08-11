"""Added users to transactions

Revision ID: f7d8a7df088a
Revises: cfb6f172bc9b
Create Date: 2019-08-10 20:30:58.548859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7d8a7df088a'
down_revision = 'cfb6f172bc9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('line_item', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'line_item', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'line_item', type_='foreignkey')
    op.drop_column('line_item', 'user_id')
    # ### end Alembic commands ###
