"""empty message

Revision ID: b1389ea3371e
Revises: b34bc7e14e6a
Create Date: 2019-04-28 10:50:06.560517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b1389ea3371e'
down_revision = 'b34bc7e14e6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'material_detail', ['物料ID'])
    op.drop_column('material_detail', '材质')
    op.drop_column('material_detail', '密度')
    op.drop_column('material_detail', 'jackddd')
    op.drop_column('material_detail', 'oooo')
    op.drop_column('material_detail', 'bear')
    op.drop_column('material_detail', 'jack')
    op.drop_column('material_detail', '浓度')
    op.drop_column('material_detail', 'bearandxun')
    op.drop_column('material_detail', 'Bigbang')
    op.drop_column('material_detail', 'ADAddd')
    op.drop_column('material_detail', 'bbgsdgsdhs')
    op.drop_column('material_detail', 'afaffsgs')
    op.drop_column('material_detail', '赛亚人')
    op.drop_column('material_detail', 'dd')
    op.drop_column('material_detail', 'bb')
    op.drop_column('material_detail', 'xiaoxun')
    op.drop_column('material_detail', '高安市')
    op.drop_column('materials', '物料价格')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('物料价格', mysql.FLOAT(), nullable=True))
    op.add_column('material_detail', sa.Column('高安市', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('xiaoxun', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('bb', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('dd', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('赛亚人', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('afaffsgs', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('bbgsdgsdhs', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('ADAddd', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('Bigbang', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('bearandxun', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('浓度', mysql.FLOAT(), nullable=True))
    op.add_column('material_detail', sa.Column('jack', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('bear', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('oooo', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('jackddd', mysql.VARCHAR(length=10), nullable=True))
    op.add_column('material_detail', sa.Column('密度', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.add_column('material_detail', sa.Column('材质', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'material_detail', type_='unique')
    # ### end Alembic commands ###
