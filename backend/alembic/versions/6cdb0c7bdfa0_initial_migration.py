"""initial migration

Revision ID: 6cdb0c7bdfa0
Revises: 
Create Date: 2022-04-30 12:39:11.792308

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '6cdb0c7bdfa0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False, autoincrement=True, primary_key=True),
                    sa.Column('first_name', sa.String, default=None, nullable=True),
                    sa.Column('last_name', sa.String, default=None, nullable=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('hashed_password', sa.String, nullable=False),
                    sa.Column('is_active', sa.Boolean, nullable=False, server_default=sa.text('true')),
                    sa.Column('is_superuser', sa.Boolean, nullable=False, server_default=sa.text('false')),
                    sa.Column('created_at', sa.DateTime, nullable=False),
                    sa.Column('updated_at', sa.DateTime, nullable=False),
                    sa.Column('deleted_at', sa.DateTime, nullable=True, default=None),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_index('users_email_idx', 'users', ['email'], unique=True)
    op.create_index('users_first_name_idx', 'users', ['first_name'])
    op.create_index('users_last_name_idx', 'users', ['last_name'])


def downgrade():
    op.drop_index('users_last_name_idx', table_name='users')
    op.drop_index('users_first_name_idx', table_name='users')
    op.drop_index('users_email_idx', table_name='users')
    op.drop_table('users')
