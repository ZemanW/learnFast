"""create post

Revision ID: e61925a229c9
Revises: 6172d7bb8107
Create Date: 2026-01-15 14:16:36.527235

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e61925a229c9"
down_revision = "6172d7bb8107"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
    )

    pass


def downgrade():
    op.drop_table("posts")
    pass
