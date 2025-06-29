"""2

Revision ID: ee975412e691
Revises: af7e95b0af53
Create Date: 2025-06-19 22:04:35.875383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ee975412e691'
down_revision: Union[str, None] = 'af7e95b0af53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('foods', 'product_name',
               existing_type=postgresql.ENUM('OATMEAL', 'APPLE', 'BANANA', 'BREAD', 'MUFFINS', 'PANCAKE', 'OMELETTE', 'RICE', 'POTATO_WEDGES', 'FRIES', 'GLAZED_CARROT', 'MACARONI', 'CRUSTED_CHICKEN', 'CUCUMBER', 'BEET', 'SUNNY_SIDEUP_EGG', 'CHICKEN', 'CHEESE', 'SALAD', 'ORANGE', 'GRAPES', 'CARROT', 'TOMATO', 'LETTUCE', name='product'),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('foods', 'product_name',
               existing_type=sa.String(),
               type_=postgresql.ENUM('OATMEAL', 'APPLE', 'BANANA', 'BREAD', 'MUFFINS', 'PANCAKE', 'OMELETTE', 'RICE', 'POTATO_WEDGES', 'FRIES', 'GLAZED_CARROT', 'MACARONI', 'CRUSTED_CHICKEN', 'CUCUMBER', 'BEET', 'SUNNY_SIDEUP_EGG', 'CHICKEN', 'CHEESE', 'SALAD', 'ORANGE', 'GRAPES', 'CARROT', 'TOMATO', 'LETTUCE', name='product'),
               existing_nullable=False)
    # ### end Alembic commands ###
