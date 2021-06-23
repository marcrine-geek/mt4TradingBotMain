"""empty message

Revision ID: 3347b18006e1
Revises: 29a1aaeb5a18
Create Date: 2021-06-18 15:02:39.897375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3347b18006e1'
down_revision = '29a1aaeb5a18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('verification_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=120), nullable=False),
    sa.Column('phone', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('phone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('verification_code')
    # ### end Alembic commands ###