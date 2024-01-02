from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://telkestech%40gmail.com:ShXixZT5YV6u@ep-red-bird-68334114.ap-southeast-1.aws.neon.tech/GeoServiceability?sslmode=require'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

Base = declarative_base()
