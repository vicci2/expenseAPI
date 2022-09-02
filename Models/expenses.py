# This file is used to scalulpt the Expenses Model/Table in the system Database:

from sqlalchemy import Column,Integer,DateTime,NUMERIC, String,func,ForeignKey
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... so:
from db.base import Base

# The Sales Model:
class Expenses(Base):
    # attaching a prefered tablename:
    __tablename__='expenses'
    # Column defination:
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("user.id"))
    expense=Column(String,nullable=False)
    quantity=Column(NUMERIC,nullable=False)   
    cost=Column(NUMERIC,nullable=False)   
    date=Column(DateTime(timezone=False),server_default=func.now())
    
    user=relationship("User",back_populates="expenses")# relationship defination:child
