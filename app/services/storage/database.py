import os

import sqlalchemy
from databases import Database
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)

engine = sqlalchemy.create_engine(DATABASE_URL)

Base = declarative_base()


async def create_tables():
    Base.metadata.create_all(bind=engine)
