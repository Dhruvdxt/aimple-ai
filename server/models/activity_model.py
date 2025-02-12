from enum import Enum as PyEnum
from sqlalchemy import Table, Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from ..config.db_config import meta


class ActivityType(str, PyEnum):
    REGISTRATION = "REGISTRATION"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    UPDATE_PROFILE = "UPDATE_PROFILE"
    PASSWORD_RESET = "PASSWORD_RESET"
    ACCOUNT_DELETE = "ACCOUNT_DELETE"
    ENABLE_OR_DISABLE = "ENABLE_OR_DISABLE"
    EMAIL_VERIFIED = "EMAIL_VERIFIED"
    MFA_ENABLED = "MFA_ENABLED"
    MFA_DISABLED = "MFA_DISABLED"
 
activity = Table(
    "activity", meta,
    Column('id', Integer, autoincrement=True, primary_key=True),
    Column('session_id', String(255), nullable=True),
    Column('user_id', Integer, nullable=True),
    Column('activity_type', Enum(ActivityType), nullable=False),
    Column('timestamp', DateTime, default=func.now())
)