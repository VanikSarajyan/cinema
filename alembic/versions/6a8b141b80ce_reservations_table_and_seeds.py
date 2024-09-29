"""Reservations table and seeds

Revision ID: 6a8b141b80ce
Revises: c95f42f16093
Create Date: 2024-09-29 13:09:09.733507

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision: str = "6a8b141b80ce"
down_revision: Union[str, None] = "c95f42f16093"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("schedule_id", sa.Integer, sa.ForeignKey("schedules.id"), nullable=False),
        sa.Column("seat_id", sa.Integer, sa.ForeignKey("seats.id"), nullable=False),
    )

    reservations_table = table(
        "reservations",
        column("id", Integer),
        column("user_id", Integer),
        column("schedule_id", Integer),
        column("seat_id", Integer),
    )

    op.bulk_insert(
        reservations_table,
        [
            {"id": 1, "user_id": 1, "schedule_id": 1, "seat_id": 1},
            {"id": 2, "user_id": 1, "schedule_id": 1, "seat_id": 2},
            {"id": 3, "user_id": 2, "schedule_id": 2, "seat_id": 3},
        ],
    )


def downgrade():
    op.drop_table("reservations")
