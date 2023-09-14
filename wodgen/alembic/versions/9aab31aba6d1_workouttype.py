"""WorkoutType

Revision ID: 9aab31aba6d1
Revises: 75ea943e7f68
Create Date: 2023-09-09 12:43:01.764824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aab31aba6d1'
down_revision: Union[str, None] = '75ea943e7f68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
