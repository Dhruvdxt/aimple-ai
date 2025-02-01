from sqlalchemy import Table, Column, Integer, String, Boolean
from ..config.db_config import meta

users = Table(
    "users", meta,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('email', String(255)),
    Column('full_name', String(255), default="NA"),
    Column('hashed_password', String(255)),
    Column('disabled', Boolean, default=False)
)