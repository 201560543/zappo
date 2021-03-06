"""empty message

Revision ID: 49d113d7a36b
Revises: 
Create Date: 2020-04-24 20:38:57.030399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49d113d7a36b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('account_number', sa.String(length=32), nullable=True),
    sa.Column('invoice_number', sa.String(length=32), nullable=False),
    sa.Column('invoice_term_name', sa.String(length=32), nullable=True),
    sa.Column('invoice_date', sa.String(length=32), nullable=True),
    sa.Column('supplier', sa.String(length=32), nullable=True),
    sa.Column('customer_account_number', sa.String(length=32), nullable=True),
    sa.Column('vendor', sa.String(length=32), nullable=True),
    sa.Column('order_items', sa.String(length=32), nullable=True),
    sa.Column('raw_sold_to_info', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('invoice_number')
    )
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
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstName', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_firstName'), 'user', ['firstName'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_firstName'), table_name='user')
    op.drop_table('user')
    op.drop_table('order_item')
    op.drop_table('order')
    # ### end Alembic commands ###
