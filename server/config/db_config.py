from fastapi import HTTPException, status
from sqlalchemy import create_engine, MetaData
from os import getenv
import redis.asyncio as rd
import urllib.parse


# MySQL
mysql_user = getenv('MYSQL_USER')
encoded_password = urllib.parse.quote(getenv('MYSQL_CONN_PASSWORD'))
mysql_host = getenv('MYSQL_HOST')
mysql_db_name = getenv('MYSQL_DB_NAME')
DATABASE_URL = f"mysql+pymysql://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db_name}"

engine = create_engine(DATABASE_URL, echo=True)
meta = MetaData()
db = engine.connect()


# Redis
redis = None

def init_redis():
    try:
        global redis
        redis = rd.Redis(host=getenv('REDIS_HOST'), port=getenv('REDIS_PORT'), decode_responses=True)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
init_redis()
