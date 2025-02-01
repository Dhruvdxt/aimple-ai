from ..config.db_config import meta, engine
from .admin_model import admins
from .user_model import users

# creating all tables
meta.create_all(engine)