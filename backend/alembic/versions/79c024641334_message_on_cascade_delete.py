"""Message on cascade delete

Revision ID: 79c024641334
Revises: c411223c3deb
Create Date: 2025-04-11 00:28:14.075612

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79c024641334'
down_revision: Union[str, None] = 'c411223c3deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('messages_topic_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'topics', ['topic_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_topic_id_fkey', 'messages', 'topics', ['topic_id'], ['id'])
    # ### end Alembic commands ###
