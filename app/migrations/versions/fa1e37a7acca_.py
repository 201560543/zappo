"""empty message

Revision ID: fa1e37a7acca
Revises: 49d113d7a36b
Create Date: 2020-04-26 17:22:55.153219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa1e37a7acca'
down_revision = '49d113d7a36b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('account')
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('account',
    sa.Column('id', mysql.INTEGER(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('organization_id', mysql.INTEGER(unsigned=True), autoincrement=False, nullable=False, comment='An organization can have one or multimple account accross time. Account could be closed. Another one opened.'),
    sa.Column('account_number', mysql.CHAR(length=32), nullable=False, comment='Possible account number (auto-generated)'),
    sa.Column('account_name', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('is_active', mysql.TINYINT(unsigned=True), server_default=sa.text("'1'"), autoincrement=False, nullable=False, comment='Allow track if account is active or de-activated (non payment). Inactive account cannot login.'),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.Column('is_deleted', mysql.TINYINT(unsigned=True), server_default=sa.text("'0'"), autoincrement=False, nullable=False),
    sa.Column('timezone_name', mysql.VARCHAR(length=50), nullable=False, comment='Timezone of the account.'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
