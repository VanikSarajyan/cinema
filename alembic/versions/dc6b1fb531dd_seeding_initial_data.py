"""Seeding initial data

Revision ID: dc6b1fb531dd
Revises: fd631c03cecf
Create Date: 2024-09-25 12:55:37.896933

"""

from typing import Sequence, Union

from alembic import op

from app.security import get_password_hash


# revision identifiers, used by Alembic.
revision: str = "dc6b1fb531dd"
down_revision: Union[str, None] = "bc25c1e6d8e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        f"""
        INSERT INTO users (id, username, email, hashed_password, role) VALUES
        (1, 'admin', 'admin@example.com', '{get_password_hash("admin")}', 'admin'),
        (2, 'user', 'user@example.com', '{get_password_hash("user")}', 'regular')
    """
    )


def downgrade() -> None:
    op.execute("DELETE FROM users")
