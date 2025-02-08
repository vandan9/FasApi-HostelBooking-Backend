"""adding payment column

Revision ID: 11dc48a0c2ed
Revises: 26b72c0e7466
Create Date: 2024-07-15 22:23:57.129918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '11dc48a0c2ed'
down_revision: Union[str, None] = '26b72c0e7466'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    op.add_column('bookings', sa.Column('payment', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'payment')
    op.create_table('payments',
    sa.Column('payment_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('booking_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('amount', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('create_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.booking_id'], name='payments_booking_id_fkey'),
    sa.PrimaryKeyConstraint('payment_id', name='payments_pkey')
    )
    # ### end Alembic commands ###
