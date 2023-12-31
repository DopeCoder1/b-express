"""dsds

Revision ID: a9a3bc49bfcb
Revises: 954e2bce12e6
Create Date: 2024-01-04 12:11:56.428311

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a3bc49bfcb'
down_revision: Union[str, None] = '954e2bce12e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order_items', sa.Column('description', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('sender_fio', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('sender_phone', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('reciever_fio', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('reciever_phone', sa.String(), nullable=False))
    op.add_column('orders', sa.Column('insurance', sa.DECIMAL(precision=10, scale=2), nullable=False))
    op.drop_constraint('orders_sender_fkey', 'orders', type_='foreignkey')
    op.drop_constraint('orders_reciever_fkey', 'orders', type_='foreignkey')
    op.drop_column('orders', 'reciever')
    op.drop_column('orders', 'sender')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('sender', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('orders', sa.Column('reciever', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('orders_reciever_fkey', 'orders', 'users', ['reciever'], ['id'])
    op.create_foreign_key('orders_sender_fkey', 'orders', 'users', ['sender'], ['id'])
    op.drop_column('orders', 'insurance')
    op.drop_column('orders', 'reciever_phone')
    op.drop_column('orders', 'reciever_fio')
    op.drop_column('orders', 'sender_phone')
    op.drop_column('orders', 'sender_fio')
    op.drop_column('order_items', 'description')
    # ### end Alembic commands ###
