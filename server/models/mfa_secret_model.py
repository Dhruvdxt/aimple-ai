from sqlalchemy import Table, Column, Integer, String
from ..config.db_config import meta

mfa_secret = Table(
    "mfa_secret", meta,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('secret', String(255), nullable=False)
)