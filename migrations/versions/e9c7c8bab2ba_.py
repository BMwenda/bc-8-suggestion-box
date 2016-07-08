"""empty message

Revision ID: e9c7c8bab2ba
Revises: c75c82881c28
Create Date: 2016-06-24 09:42:48.967878

"""

# revision identifiers, used by Alembic.
revision = 'e9c7c8bab2ba'
down_revision = 'c75c82881c28'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('comment', sa.String(length=140), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'comment')
    ### end Alembic commands ###