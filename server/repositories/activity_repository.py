from sqlalchemy import Enum
from ..config.db_config import db
from ..models.index import activity, ActivityType


def create_activity(user_id: int, admin_id: int, activity_type: Enum, ip_address: str):
    db.execute(activity.insert().values(
        user_id=user_id,
        admin_id=admin_id,
        activity_type=activity_type,
        ip_address=ip_address
    ))
    db.commit()
    # db.refresh(db_user)