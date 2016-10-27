from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('about_me', VARCHAR(length=140)),
    Column('authenticated', BOOLEAN),
    Column('last_seen', DATETIME),
    Column('password', VARCHAR),
    Column('profile_img', VARCHAR(length=256)),
    Column('username', VARCHAR(length=64)),
)

user = Table('user', post_meta,
    Column('password', String),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('about_me', String(length=140)),
    Column('profile_img', String(length=256)),
    Column('last_seen', DateTime),
    Column('authenticated', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].drop()
    post_meta.tables['user'].columns['nickname'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['user'].columns['username'].create()
    post_meta.tables['user'].columns['nickname'].drop()
