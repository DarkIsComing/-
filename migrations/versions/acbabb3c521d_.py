"""empty message

Revision ID: acbabb3c521d
Revises: b872fd9bb6a6
Create Date: 2019-04-17 13:06:09.448290

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'acbabb3c521d'
down_revision = 'b872fd9bb6a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('adjust', '调整类型')
    op.drop_column('inventory_flow', '价格')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inventory_flow', sa.Column('价格', mysql.FLOAT(), nullable=False))
    op.add_column('adjust', sa.Column('调整类型', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
