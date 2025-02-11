from sqlalchemy import Table, Column, Integer, String,Boolean, DateTime
from ..config.db_config import meta

session = Table(
    "session", meta,
    Column('session_id', String(255), primary_key=True),
    Column('user_id', Integer, nullable=True),
    Column('admin_id', Integer, nullable=True),
    Column('is_admin', Boolean, default=False),
    Column('ip_address', String(255), nullable=True),
    Column('device', String(255), nullable=True),
    Column('created_at', DateTime),
    Column('expired_at', DateTime)
)