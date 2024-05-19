import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PDF(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String,unique=True, index=True)
    upload_date = Column(DateTime)
    text = Column(Text)

SQL_ALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
print(SQL_ALCHEMY_DATABASE_URL)

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# Create the table in the database
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)