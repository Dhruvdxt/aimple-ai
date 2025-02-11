from sqlalchemy import Table, Column, Integer, String, Boolean
from ..config.db_config import meta

user = Table(
    "user", meta,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('email', String(255)),
    Column('hashed_password', String(255)),
    Column('full_name', String(255), default="NA"),
    Column('phone', String(255), default="NA"),
    Column('address', String(255), default="NA"),
    Column('country', String(255), default="NA"),
    Column('disabled', Boolean, default=False),
    Column('verified', Boolean, default=False),
    Column('is_mfa_enabled', Boolean, default=False),
)