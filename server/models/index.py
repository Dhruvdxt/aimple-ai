from ..config.db_config import meta, engine
from .admin_model import admin
from .user_model import user

# creating all tables
meta.create_all(engine)