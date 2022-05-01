"""create editor elements table

Revision ID: 5b9a6c625c53
Revises: c139d77f3e66
Create Date: 2022-04-30 15:38:11.636950

"""
import enum

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Enum


class ContentType(enum.Enum):
    HEADING = 'HEADING'
    ACTION = 'ACTION'
    CHARACTER = 'CHARACTER'
    PARENTHETICAL = 'PARENTHETICAL'
    DIALOGUE = 'DIALOGUE'
    SHOT = 'SHOT'
    TRANSITION = 'TRANSITION'
    TEXT = 'TEXT'


# revision identifiers, used by Alembic.
revision = '5b9a6c625c53'
down_revision = 'c139d77f3e66'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'editorelements',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('content', sa.String, nullable=True),
        sa.Column('content_type', Enum(ContentType), nullable=True, default='TEXT'),
        sa.Column('position', sa.Integer, nullable=False, default=0),

        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.text('now()')),
        sa.Column('deleted_at', sa.DateTime, nullable=True, default=None),

        sa.PrimaryKeyConstraint('id'),

        sa.Column('screenplay_id', sa.Integer, nullable=False, index=True),
        sa.ForeignKeyConstraint(('screenplay_id',), ['screenplays.id'], ondelete='CASCADE'),
    )

    op.create_index('editor_element_content_idx', 'editorelements', ['content'])
    op.create_index('editor_element_content_type_idx', 'editorelements', ['content_type'])


def downgrade():
    sa.ForeignKeyConstraint(('screenplay_id',), ['screenplays.id'], ondelete='CASCADE').drop()
    op.drop_index('editor_element_content_idx', table_name='editorelements')
    op.drop_index('editor_element_content_type_idx', table_name='editorelements')
    op.drop_table('editorelements')
