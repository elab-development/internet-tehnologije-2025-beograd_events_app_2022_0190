"""Dodavanje check constraint za cenu

Revision ID: 0ac698f866b7
Revises: 2e8a9d95107a
Create Date: 2026-02-03 22:50:46.275446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ac698f866b7'
down_revision = '2e8a9d95107a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        "check_cena_positive",
        "dogadjaj",
        "cena >= 0"
    )

def downgrade():
    op.drop_constraint(
        "check_cena_positive",
        "dogadjaj",
        type_="check"
    )

