"""empty message

Revision ID: be884dddefdb
Revises: e4b556adde53
Create Date: 2022-02-11 06:27:49.725183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be884dddefdb'
down_revision = 'e4b556adde53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'timestamp')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('timestamp', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
