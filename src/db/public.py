import sqlalchemy as sa


meta = sa.MetaData(schema='public')


books = sa.Table(
    'books', meta,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('filename', sa.Text, nullable=False),
    sa.Column('cover', sa.Text, nullable=False),
    sa.Column('file', sa.Text, nullable=False),
    sa.Column('title', sa.Text),
)

tags = sa.Table(
    'tags', meta,
    sa.Column('id', sa.BigInteger, primary_key=True),
    sa.Column('name', sa.Text, nullable=False),
)

m2m_tag_book = sa.Table(
    'm2m_tag_book', meta,
    sa.Column('book_id', sa.BigInteger, nullable=False),
    sa.Column('tag_id', sa.BigInteger, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], 'fk_m2m_tag_book_on_book', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], 'fk_m2m_tag_book_on_tag', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('book_id', 'tag_id', name='pk_m2m_tag_book'),
)
