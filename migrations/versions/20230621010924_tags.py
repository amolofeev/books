"""tags

Revision ID: febcb52fe13c
Revises: cf94ec60e0d4
Create Date: 2023-06-21 01:09:24.308597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'febcb52fe13c'
down_revision = 'cf94ec60e0d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tags',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='public'
    )
    op.create_table('m2m_tag_book',
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.Column('tag_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['public.books.id'], name='fk_m2m_tag_book_on_book', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['public.tags.id'], name='fk_m2m_tag_book_on_tag', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('book_id', 'tag_id', name='pk_m2m_tag_book'),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('m2m_tag_book', schema='public')
    op.drop_table('tags', schema='public')
    # ### end Alembic commands ###
