"""empty message

Revision ID: 61d991138ef4
Revises: bf0b8697ae9a
Create Date: 2022-02-11 09:38:12.364519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61d991138ef4'
down_revision = 'bf0b8697ae9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scored__game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date_played', sa.Date(), nullable=True),
    sa.Column('number_of_players', sa.Integer(), nullable=True),
    sa.Column('starting_position', sa.Integer(), nullable=True),
    sa.Column('auto_or_manual', sa.Boolean(), nullable=True),
    sa.Column('file_name', sa.String(length=120), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scored__game')
    # ### end Alembic commands ###