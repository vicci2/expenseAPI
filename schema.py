from pydantic import BaseModel
from typing import Optional, List 
from datetime import datetime

# Expenses schema:
class ExpenseBase(BaseModel):
    userId:int
    expense:str
    quantity:int
    cost:int

class CreateExpense(ExpenseBase):
    pass

class ExpensePut(BaseModel):
    userID: Optional[int]
    expense: Optional[str]
    quantity: Optional[int]
    cost: Optional[int]            

class Expense(ExpenseBase):
    class Config:
        orm_mode=True

class ExpenseInDb(ExpenseBase):
    # id:int
    # created:datetime
    class Config:
        orm_mode=True

# User Schema:
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class CreateUser(UserBase):
    pass

class UserPut(UserBase):
    first_name:Optional[str]
    last_name:Optional[str]
    email:Optional[str]

class UserInfo(UserBase):
    id:int
    class Config:
        orm_mode=True

class UserInDb(UserBase):
    id:int
    created:datetime
    todos:list[Expense]
    users:UserInfo
    class Config:
        orm_mode=True
