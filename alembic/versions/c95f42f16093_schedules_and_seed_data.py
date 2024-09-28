"""schedules and seed data

Revision ID: c95f42f16093
Revises: ff34bd0361c2
Create Date: 2024-09-28 21:00:34.501663

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = "c95f42f16093"
down_revision: Union[str, None] = "ff34bd0361c2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "schedule",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("movie_id", sa.Integer, sa.ForeignKey("movies.id", ondelete="CASCADE")),
        sa.Column("room_id", sa.Integer, sa.ForeignKey("rooms.id", ondelete="CASCADE")),
        sa.Column("start_time", sa.DateTime, nullable=False),
        sa.Column("end_time", sa.DateTime, nullable=False),
    )

    schedule_table = table(
        "schedule",
        column("movie_id", sa.Integer),
        column("room_id", sa.Integer),
        column("start_time", sa.DateTime),
        column("end_time", sa.DateTime),
    )

    op.bulk_insert(
        schedule_table,
        [
            {
                "movie_id": 1,
                "room_id": 1,
                "start_time": datetime(2024, 10, 1, 18, 0),
                "end_time": datetime(2024, 10, 1, 20, 0),
            },
            {
                "movie_id": 2,
                "room_id": 1,
                "start_time": datetime(2024, 10, 1, 20, 0),
                "end_time": datetime(2024, 10, 1, 22, 0),
            },
            {
                "movie_id": 1,
                "room_id": 3,
                "start_time": datetime(2024, 10, 2, 15, 0),
                "end_time": datetime(2024, 10, 2, 17, 0),
            },
            {
                "movie_id": 1,
                "room_id": 2,
                "start_time": datetime(2024, 10, 2, 14, 0),
                "end_time": datetime(2024, 10, 2, 16, 0),
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("schedule")
