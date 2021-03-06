from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
portfolio_item = Table('portfolio_item', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('description', VARCHAR),
    Column('markdown', VARCHAR),
    Column('name', VARCHAR(length=35)),
    Column('artwork_path', VARCHAR(length=256)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['portfolio_item'].columns['markdown'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['portfolio_item'].columns['markdown'].create()
