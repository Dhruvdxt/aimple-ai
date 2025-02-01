from ..config.db_config import db
from ..models.index import admins

def get_admin_by_email(email: str):
    return db.execute(admins.select().where(admins.c.email==email)).fetchone()

# To do:
# 1. Exception handling