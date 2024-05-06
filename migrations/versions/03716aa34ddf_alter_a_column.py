"""Alter a column

Revision ID: 03716aa34ddf
Revises: b96ce8555b51
Create Date: 2024-05-04 20:08:44.182377

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03716aa34ddf'
down_revision: Union[str, None] = 'b96ce8555b51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
