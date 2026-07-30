"""Allow only one review per user and game.

Revision ID: 20260729_review_user_game
Revises:
Create Date: 2026-07-29
"""

from alembic import op


revision = "20260729_review_user_game"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_review_user_game",
        "reviews",
        ["user_id", "game_id"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_review_user_game", "reviews", type_="unique")
