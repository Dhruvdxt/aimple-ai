from sqlalchemy import Enum
from typing import Optional
from ..config.db_config import db
from ..models.index import activity


def create_activity(activity_type: Enum, public_ip_address: str, city: str, region: str, country: str, isp: str, session_id: Optional[str] = None, user_id: Optional[int] = None):
    data = {
        "session_id": session_id,
        "user_id": user_id,
        "activity_type": activity_type,
        "public_ip_address": public_ip_address,
        "city": city,
        "region": region,
        "country": country,
        "isp": isp
    }

    data = {key: value for key, value in data.items() if value is not None}
    
    db.execute(activity.insert().values(**data))
    db.commit()
    # db.refresh(db_user)
    
def get_all_activities():
    return db.execute(activity.select()).fetchall()

def get_activities_by_user_id(user_id: int):
    return db.execute(activity.select().where(activity.c.user_id==user_id)).fetchall()