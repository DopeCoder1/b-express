"""add new field phone for user

Revision ID: c117fd7f0043
Revises: 357e58b58e1f
Create Date: 2024-01-04 22:01:23.871624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c117fd7f0043'
down_revision: Union[str, None] = '357e58b58e1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('warehouses', sa.Column('status', sa.Boolean(), server_default='false', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('warehouses', 'status')
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
