from ..config.db_config import db
from ..models.index import mfa_secret

def create_mfa_secret(user_id: int, secret: str):
    db.execute(mfa_secret.insert().values(
        user_id=user_id,
        secret=secret
    ))
    db.commit()
    return
    # db.refresh(db_user)
    
def get_mfa_secret_by_user_id(user_id: int):
    return db.execute(mfa_secret.select().where(mfa_secret.c.user_id==user_id)).fetchone()


def delete_mfa_secret_by_user_id(user_id: int):
    db.execute(mfa_secret.delete().where(mfa_secret.c.user_id==user_id))
    db.commit()