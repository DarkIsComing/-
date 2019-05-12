"""empty message

Revision ID: 745ece127f2c
Revises: 9494b2033d55
Create Date: 2019-04-26 17:06:24.130402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '745ece127f2c'
down_revision = '9494b2033d55'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adjust',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('调整日期', sa.DateTime(), nullable=True),
    sa.Column('调整数据', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('buy_order',
    sa.Column('进货id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('进货数量', sa.Integer(), nullable=False),
    sa.Column('进货价格', sa.Float(), nullable=False),
    sa.Column('进货日期', sa.DateTime(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('进货id')
    )
    op.create_table('inventory',
    sa.Column('库存编号', sa.Integer(), nullable=False),
    sa.Column('类型', sa.Enum('in', 'out', 'adjust'), nullable=True),
    sa.Column('发生数量', sa.Integer(), nullable=True),
    sa.Column('库存数量', sa.Integer(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('库存编号')
    )
    op.create_table('inventory_flow',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('日期', sa.DateTime(), nullable=True),
    sa.Column('类型', sa.Enum('in', 'out', 'adjust'), nullable=True),
    sa.Column('发生数量', sa.Integer(), nullable=False),
    sa.Column('库存数量', sa.Integer(), nullable=False),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('sale_order',
    sa.Column('出货id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('出货数量', sa.Integer(), nullable=False),
    sa.Column('出货价格', sa.Float(), nullable=False),
    sa.Column('出货日期', sa.DateTime(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('出货id')
    )
    op.create_table('stock_in',
    sa.Column('入库单id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('入库数量', sa.Integer(), nullable=False),
    sa.Column('入库价格', sa.Float(), nullable=False),
    sa.Column('入库日期', sa.DateTime(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('入库单id')
    )
    op.create_table('stock_out',
    sa.Column('出库单id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('出库数量', sa.Integer(), nullable=False),
    sa.Column('出库价格', sa.Float(), nullable=False),
    sa.Column('出库日期', sa.DateTime(), nullable=True),
    sa.Column('物料名称', sa.String(length=64), nullable=True),
    sa.Column('物料ID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['物料ID'], ['materials.ID'], ),
    sa.PrimaryKeyConstraint('出库单id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stock_out')
    op.drop_table('stock_in')
    op.drop_table('sale_order')
    op.drop_table('inventory_flow')
    op.drop_table('inventory')
    op.drop_table('buy_order')
    op.drop_table('adjust')
    # ### end Alembic commands ###
