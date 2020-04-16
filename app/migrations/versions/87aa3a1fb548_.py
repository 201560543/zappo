"""empty message

Revision ID: 87aa3a1fb548
Revises: eb2a44f1a243
Create Date: 2020-04-16 01:47:01.049892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87aa3a1fb548'
down_revision = 'eb2a44f1a243'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order_item',
    sa.Column('order_item_id', sa.String(length=32), nullable=False),
    sa.Column('item_number', sa.String(length=32), nullable=True),
    sa.Column('order_quantity', sa.String(length=32), nullable=True),
    sa.Column('shipped_quantity', sa.String(length=32), nullable=True),
    sa.Column('unit', sa.String(length=32), nullable=True),
    sa.Column('size', sa.String(length=32), nullable=True),
    sa.Column('brand', sa.String(length=32), nullable=True),
    sa.Column('description', sa.String(length=32), nullable=True),
    sa.Column('weight', sa.String(length=32), nullable=True),
    sa.Column('price', sa.String(length=32), nullable=True),
    sa.Column('total_price', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('order_item_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item')
    # ### end Alembic commands ###
