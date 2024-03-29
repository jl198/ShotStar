"""empty message

Revision ID: 310bbc302d01
Revises: 61d991138ef4
Create Date: 2022-02-11 09:40:38.277980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '310bbc302d01'
down_revision = '61d991138ef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scored__game', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'scored__game', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'scored__game', type_='foreignkey')
    op.drop_column('scored__game', 'user_id')
    # ### end Alembic commands ###
