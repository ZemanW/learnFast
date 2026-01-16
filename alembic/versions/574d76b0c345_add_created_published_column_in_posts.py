"""add created,published column in posts

Revision ID: 574d76b0c345
Revises: 1c30fa92c5cd
Create Date: 2026-01-15 14:32:42.598964

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "574d76b0c345"
down_revision = "1c30fa92c5cd"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.BOOLEAN,
            nullable=False,
            server_default=sa.text("true"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
