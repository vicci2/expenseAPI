# This file is used to scalulpt the Expenses Model/Table in the system Database:

from sqlalchemy import Column,Integer,String,DateTime,Text,NUMERIC,func
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... so:
from db.base import  Base

# Users class:
class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String ,nullable=False)
    last_name=Column(String ,nullable=False)
    email=Column(String ,nullable=False,unique=True)   
    date=Column(DateTime(timezone=False),server_default=func.now())

    expenses=relationship("Expenses",back_populates="user")# relationship defination:parent