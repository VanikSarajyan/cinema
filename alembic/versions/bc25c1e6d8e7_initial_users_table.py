"""Initial Users table

Revision ID: bc25c1e6d8e7
Revises: 
Create Date: 2024-09-25 22:12:50.622751

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc25c1e6d8e7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("email", sa.VARCHAR(), nullable=False),
        sa.Column("username", sa.VARCHAR(), nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(), nullable=True),
        sa.Column("role", sa.VARCHAR(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_index("ix_users_email", "users", ["email"], unique=1)


def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
