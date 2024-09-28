"""seats table with seed data

Revision ID: ff34bd0361c2
Revises: a142782d0d77
Create Date: 2024-09-28 18:29:58.867713

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision: str = "ff34bd0361c2"
down_revision: Union[str, None] = "a142782d0d77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "seats",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("room_id", sa.Integer, sa.ForeignKey("rooms.id", ondelete="CASCADE")),
        sa.Column("row_number", sa.Integer, nullable=False),
        sa.Column("column_number", sa.Integer, nullable=False),
    )

    seats_table = table(
        "seats",
        column("id", sa.Integer),
        column("room_id", sa.Integer),
        column("row_number", sa.Integer),
        column("column_number", sa.Integer),
    )

    conn = op.get_bind()

    inspector = Inspector.from_engine(conn)
    if "rooms" not in inspector.get_table_names():
        raise RuntimeError("The 'rooms' table does not exist.")

    conn = op.get_bind()

    rooms_query = conn.execute(sa.text("SELECT id, rows, columns FROM rooms"))

    seats = []
    for room in rooms_query:
        room_id, num_rows, num_columns = room

        for row in range(1, num_rows + 1):
            for seat in range(1, num_columns + 1):
                seats.append(
                    {
                        "room_id": room_id,
                        "row_number": row,
                        "column_number": seat,
                    }
                )

    op.bulk_insert(seats_table, seats)


def downgrade():
    op.drop_table("seats")
