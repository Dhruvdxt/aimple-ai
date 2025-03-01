from sqlalchemy import Table, Column, Integer, String, Boolean
from ..config.db_config import meta

settings = Table(
    "settings", meta,
    Column('name', String(255), nullable=False, primary_key=True),
    Column('value', String(255), nullable=False),
)