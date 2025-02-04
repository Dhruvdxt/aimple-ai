from ..config.db_config import meta, engine
from .admin_model import *
from .user_model import *
from .activity_model import *

# creating all tables
meta.create_all(engine)