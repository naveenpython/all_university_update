from sqlmodel import SQLModel, Field, create_engine, Session
from sqlalchemy import Column, Text  # Yeh naya import add kiya hai
from typing import Optional
from datetime import datetime

# Apna wahi purana DATABASE_URL rakhna jo chal raha tha
DATABASE_URL = "mysql+mysqlconnector://root:Naveen7549%40@localhost:3306/university_update_db"

engine = create_engine(DATABASE_URL, echo=True)

class University(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    state: str
    website_url: str

class Notice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    university_id: int = Field(foreign_key="university.id")
    # NAYA CHANGE: Inko limit free (Text) kar diya taaki kitna bhi lamba URL aa jaye, error na aaye
    title: str = Field(sa_column=Column(Text)) 
    link: str = Field(sa_column=Column(Text))
    date_published: datetime = Field(default_factory=datetime.utcnow)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session