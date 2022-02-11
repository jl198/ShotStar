"""empty message

Revision ID: e482db435c60
Revises: 310bbc302d01
Create Date: 2022-02-11 09:41:14.925028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e482db435c60'
down_revision = '310bbc302d01'
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
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scored__game')
    # ### end Alembic commands ###
