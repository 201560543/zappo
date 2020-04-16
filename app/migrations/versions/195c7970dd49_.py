"""empty message

Revision ID: 195c7970dd49
Revises: edccf511592b
Create Date: 2020-04-16 00:32:00.207093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '195c7970dd49'
down_revision = 'edccf511592b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user1',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('firstName', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user1_firstName'), 'user1', ['firstName'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user1_firstName'), table_name='user1')
    op.drop_table('user1')
    # ### end Alembic commands ###
