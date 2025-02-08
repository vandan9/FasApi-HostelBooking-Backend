"""adding ratting colume in vote table

Revision ID: 169807c1dbb1
Revises: 65dbd258c9d7
Create Date: 2024-07-09 22:06:42.272823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '169807c1dbb1'
down_revision: Union[str, None] = '65dbd258c9d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('votes', sa.Column('ratting', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('votes', 'ratting')
    # ### end Alembic commands ###
