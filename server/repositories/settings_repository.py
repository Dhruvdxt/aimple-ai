from sqlalchemy import case
from ..config.db_config import db
from ..models.index import settings

    
def get_all_settings():
    return db.execute(settings.select()).fetchall()

def update_settings(update_data: dict):
    db.execute(settings.update().where(settings.c.name.in_(update_data.keys())).values(value=case(*[(settings.c.name == key, val) for key, val in update_data.items()])))
    db.commit()
    