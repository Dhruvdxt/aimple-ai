from typing import Optional
from datetime import datetime, timedelta
from os import getenv
import uuid
from ..config.db_config import db
from ..models.index import session

def create_session(user_id: Optional[int] = None, admin_id: Optional[int] = None, is_admin: bool = False, ip_address: Optional[str] = None, device: Optional[str] = None):
    session_id = uuid.uuid4();
    
    db.execute(session.insert().values(
        session_id=str(session_id),
        user_id=user_id,
        admin_id=admin_id,
        is_admin=is_admin,
        ip_address=ip_address,
        
        device=device,
        created_at=datetime.now(),
        expired_at=datetime.now() + timedelta(minutes=int(getenv('SESSION_EXPIRE_MINUTES')))
    ))
    db.commit()
    
    return get_session_by_session_id(str(session_id))
    # db.refresh(db_user)
    
def get_session_by_session_id(session_id: str):
    return db.execute(session.select().where(session.c.session_id==session_id)).fetchone()


def delete_session_by_session_id(session_id: str):
    db.execute(session.delete().where(session.c.session_id==session_id))
    db.commit()