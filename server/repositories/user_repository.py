from sqlalchemy import case, func
from pydantic import EmailStr
from ..config.db_config import db
from ..models.index import user


def create_user(email: EmailStr, hashed_password: str):
    db.execute(user.insert().values(
        email=email,
        hashed_password=hashed_password
    ))
    db.commit()
    
    return get_user_by_email(email)
    # db.refresh(db_user)
    
    
def get_all_users():
    return db.execute(user.select()).fetchall()
    

def get_user_by_email(email: str):
    return db.execute(user.select().where(user.c.email==email)).fetchone()


def get_user_by_id(id: int):
    return db.execute(user.select().where(user.c.id==id)).fetchone()


def get_user_data():
    total_users_count = func.count(user.c.id).label("total_users")
    active_users_count = func.sum(case((user.c.disabled == False, 1), else_=0)).label("active_users")
    verified_users_count = func.sum(case((user.c.verified == True, 1), else_=0)).label("verified_users")
    
    return db.execute(
        user.select()
        .with_only_columns(
            total_users_count,
            active_users_count,
            verified_users_count
        )
    ).fetchone()


def update_user_profile_data_by_id(id: int, update_data: dict):
    db.execute(user.update().where(user.c.id==id).values(**update_data))
    db.commit()
    
    
def update_user_password_by_id(id: int, update_data: dict):
    db.execute(user.update().where(user.c.id==id).values(**update_data))
    db.commit()
    

def delete_user_by_id(id: int):
    db.execute(user.delete().where(user.c.id==id))
    db.commit()