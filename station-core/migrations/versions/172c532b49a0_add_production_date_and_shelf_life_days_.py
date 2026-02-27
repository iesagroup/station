"""add production_date and shelf_life_days to station_tasks

Revision ID: 172c532b49a0
Revises: 80d00e46bdc3
Create Date: 2026-02-27 16:39:01.356808

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '172c532b49a0'
down_revision: Union[str, Sequence[str], None] = '80d00e46bdc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "station_tasks",
        sa.Column("production_date", sa.Date(), nullable=True)
    )

    op.add_column(
        "station_tasks",
        sa.Column("shelf_life_days", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("station_tasks", "shelf_life_days")
    op.drop_column("station_tasks", "production_date")
