from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = 'mysql+pymysql://***:***@database-1.cv8who2rxk2v.us-east-1.rds.amazonaws.com:3306/shopper-DB'

db_engine = create_engine(DB_URL)

db_connection = db_engine.connect()

session_local = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

declarative_base = declarative_base()

# Reference: https://www.youtube.com/watch?v=zzOwU41UjTM
