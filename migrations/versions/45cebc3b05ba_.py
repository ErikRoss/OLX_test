"""empty message

Revision ID: 45cebc3b05ba
Revises: 
Create Date: 2022-09-11 16:51:38.006399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45cebc3b05ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ad', sa.Column('title', sa.String(length=240), nullable=True))
    op.add_column('ad', sa.Column('currency', sa.String(length=5), nullable=True))
    op.drop_index('ix_ad_header', table_name='ad')
    op.create_index(op.f('ix_ad_title'), 'ad', ['title'], unique=True)
    op.drop_column('ad', 'header')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ad', sa.Column('header', sa.VARCHAR(length=240), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_ad_title'), table_name='ad')
    op.create_index('ix_ad_header', 'ad', ['header'], unique=False)
    op.drop_column('ad', 'currency')
    op.drop_column('ad', 'title')
    # ### end Alembic commands ###
