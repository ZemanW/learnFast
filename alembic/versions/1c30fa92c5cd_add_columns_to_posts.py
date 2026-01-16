"""add columns to posts

Revision ID: 1c30fa92c5cd
Revises: 2f35b9459df9
Create Date: 2026-01-15 14:28:20.458970

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1c30fa92c5cd"
down_revision = "2f35b9459df9"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade():
    op.drop_constraint("posts_users_fk")
    op.drop_column("posts", "owner_id")
    pass
