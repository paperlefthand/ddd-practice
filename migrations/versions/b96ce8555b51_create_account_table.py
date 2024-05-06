"""create account table

Revision ID: b96ce8555b51
Revises:
Create Date: 2024-05-04 19:04:10.600802

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b96ce8555b51"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("name", sa.String(20), nullable=False),
        # sa.Column("password", sa.String, nullable=False),
        sa.Column("email", sa.String(50), nullable=False),
        # sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("user")
