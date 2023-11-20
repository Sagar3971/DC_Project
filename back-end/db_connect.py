from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'mysql+pymysql://root:root@localhost:3306/shopper_store'

db_engine = create_engine(DB_URL)

db_connection = db_engine.connect()

session_local = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

declarative_base = declarative_base()

# Reference: https://www.youtube.com/watch?v=zzOwU41UjTM
