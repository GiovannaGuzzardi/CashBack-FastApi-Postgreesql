"""empty message

Revision ID: d02b17e260e4
Revises: 910256a6de87
Create Date: 2024-06-30 01:59:10.301429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd02b17e260e4'
down_revision: Union[str, None] = '910256a6de87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass