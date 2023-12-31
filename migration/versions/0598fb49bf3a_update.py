"""update

Revision ID: 0598fb49bf3a
Revises: a9a3bc49bfcb
Create Date: 2024-01-04 14:00:19.888976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0598fb49bf3a'
down_revision: Union[str, None] = 'a9a3bc49bfcb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'cities', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cities', type_='unique')
    # ### end Alembic commands ###
