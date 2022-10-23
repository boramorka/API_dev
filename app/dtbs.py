from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import sttngs

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@ip-address/hostname>/<DB_NAME>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{sttngs.DB_USERNAME}:{sttngs.DB_PASSWORD}@{sttngs.DB_HOSTNAME}:{sttngs.DB_PORT}/{sttngs.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', 
#                                 dtbs='fastapi', 
#                                 user='postgres', 
#                                 password='0000',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('DB connection successeful')
#         break
#     except psycopg2.OperationalError as error:
#         print('Connecting failed')
#         print(f'error {error}')
#         print(error)
#         time.sleep(2)