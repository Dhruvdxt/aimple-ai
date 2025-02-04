from sqlalchemy import case, func
from pydantic import EmailStr
from ..config.db_config import db
from ..models.index import admin


def create_admin(email: EmailStr, hashed_password: str):
    db.execute(admin.insert().values(
        email=email,
        hashed_password=hashed_password
    ))
    db.commit()
    # db.refresh(db_admin)
    

def get_admin_by_email(email: str):
    return db.execute(admin.select().where(admin.c.email==email)).fetchone()


def get_admin_by_id(id: int):
    return db.execute(admin.select().where(admin.c.id==id)).fetchone()


def get_admin_data():
    total_admins_count = func.count(admin.c.id).label("total_admins")
    
    return db.execute(
        admin.select()
        .with_only_columns(
            total_admins_count,
        )
    ).fetchone()


def update_admin_profile_data_by_id(id: int, update_data: dict):
    db.execute(admin.update().where(admin.c.id==id).values(**update_data))
    db.commit()
    
    
def update_admin_password_by_id(id: int, update_data: dict):
    db.execute(admin.update().where(admin.c.id==id).values(**update_data))
    db.commit()
    

def delete_admin_by_id(id: int):
    db.execute(admin.delete().where(admin.c.id==id))
    db.commit()