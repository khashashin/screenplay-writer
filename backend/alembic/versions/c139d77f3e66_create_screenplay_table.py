"""create screenplay table

Revision ID: c139d77f3e66
Revises: 6cdb0c7bdfa0
Create Date: 2022-04-30 12:46:13.347463

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c139d77f3e66'
down_revision = '6cdb0c7bdfa0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'screenplays',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True, default=None),
        sa.Column('is_public', sa.Boolean, nullable=False, server_default=sa.text('false')),

        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('deleted_at', sa.DateTime, nullable=True, default=None),

        sa.PrimaryKeyConstraint('id'),

        sa.Column('owner_id', sa.Integer, nullable=False),
        sa.ForeignKeyConstraint(('owner_id',), ['users.id'], ondelete='CASCADE'),
    )

    op.create_index('screenplay_name_idx', 'screenplays', ['name'])
    op.create_index('screenplay_owner_id_idx', 'screenplays', ['owner_id'])


def downgrade():
    sa.ForeignKeyConstraint(('owner_id',), ['users.id'], ondelete='CASCADE').drop()
    op.drop_index('screenplay_owner_id_idx', table_name='screenplays')
    op.drop_index('screenplay_name_idx', table_name='screenplays')
    op.drop_table('screenplays')
