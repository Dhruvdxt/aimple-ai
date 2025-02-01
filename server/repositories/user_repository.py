from pydantic import EmailStr
from ..config.db_config import db
from ..models.index import users

def create_user(email: EmailStr, hashed_password: str):
    db.execute(users.insert().values(
        email=email,
        hashed_password=hashed_password,
    ))
    db.commit()
    # db.refresh(db_user)
    return 
    

def get_user_by_email(email: str):
    # if user_type == UserType.USER:
    return db.execute(users.select().where(users.c.email==email)).fetchone()
    # return db.query(User).filter(User.email == email).first()
# return conn.execute(admins.select().where(admins.c.email==email)).fetchall()



# To do:
# 1. Exception handling