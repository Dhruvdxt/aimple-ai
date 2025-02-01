from sqlalchemy import create_engine, MetaData
from os import getenv
import urllib.parse

user = getenv('USER')
encoded_password = urllib.parse.quote(getenv('DB_CONN_PASSWORD'))
host = getenv('HOST')
database_name = getenv('DATABASE_NAME')
DATABASE_URL = f"mysql+pymysql://{user}:{encoded_password}@{host}/{database_name}"

engine = create_engine(DATABASE_URL, echo=True)
meta = MetaData()
db = engine.connect()

def init_db():
    meta.create_all(engine)

init_db()