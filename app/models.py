from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import Integer,String,Boolean,ForeignKey

class Users(Base):
    __tablename__='users'
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    email:Mapped[str]=mapped_column(String,unique=True)
    username:Mapped[str]=mapped_column(String(100),unique=True)
    first_name:Mapped[str]=mapped_column(String(100))
    last_name:Mapped[str]=mapped_column(String(100))
    hashed_passwprd:Mapped[str]=mapped_column(String(100))
    is_active:Mapped[bool]=mapped_column(Boolean,default=True)
    role:Mapped[str]
    phone_number:Mapped[str]

class Todos(Base):
    __tablename__='todos'
    id:Mapped[int] = mapped_column(Integer,primary_key=True , index=True)
    title:Mapped[str] 
    description:Mapped[str]
    priority:Mapped[int]
    complete:Mapped[bool] = mapped_column(default=False)
    owner_id:Mapped[int]=mapped_column(Integer, ForeignKey("users.id"))
    
