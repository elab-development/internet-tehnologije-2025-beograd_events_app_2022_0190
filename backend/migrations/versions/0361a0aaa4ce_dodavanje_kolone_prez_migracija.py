"""Test migracija

Revision ID: 0361a0aaa4ce
Revises: 0ac698f866b7
Create Date: 2026-02-03 23:03:06.726142

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0361a0aaa4ce'
down_revision = '0ac698f866b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('korisnik',
        sa.Column('prezime', sa.String(length=20), nullable=True)
    )

def downgrade():
    op.drop_column('korisnik', 'prezime')

