import databases
import sqlalchemy
from sqlalchemy import create_engine, ForeignKey
from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("first_name", sqlalchemy.String(32)),
                         sqlalchemy.Column("last_name", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(16))
                         )

items = sqlalchemy.Table("items",
                         metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(50)),
                         sqlalchemy.Column("description", sqlalchemy.String(1024)),
                         sqlalchemy.Column("price", sqlalchemy.Float)
                         )


orders = sqlalchemy.Table("orders",
                          metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("id_user", sqlalchemy.Integer, ForeignKey('users.id')),
                          sqlalchemy.Column("id_item", sqlalchemy.Integer, ForeignKey('items.id')),
                          )

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
