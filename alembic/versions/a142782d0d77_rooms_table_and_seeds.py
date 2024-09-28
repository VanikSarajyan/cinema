"""Rooms table and seeds

Revision ID: a142782d0d77
Revises: b85b3fb60489
Create Date: 2024-09-27 19:12:13.415530

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a142782d0d77"
down_revision: Union[str, None] = "b85b3fb60489"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, unique=True, nullable=False),
        sa.Column("rows", sa.Integer, nullable=False),
        sa.Column("columns", sa.Integer, nullable=False),
        if_not_exists=True,
    )

    op.execute(
        """
        INSERT INTO rooms (id, name, rows, columns) VALUES
        (1, 'Red', 5, 10),
        (2, 'Green', 3, 5),
        (3, 'Blue', 4, 8)
    """
    )


def downgrade() -> None:
    op.drop_table("movies")
