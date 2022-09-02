from fastapi import APIRouter,Depends,HTTPException
from typing import List,Dict,Generator
from db.session import SessionLocal
from schema import Expense,CreateExpense,ExpensePut,ExpenseInDb
from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.expenses import Expenses
from Models.user import User

# Dependency injection:
def get_db() -> Generator:
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

expenses_router=APIRouter()

#  My Endpoints
@expenses_router.get("",
    tags=["EXPENSES"],
    # response_model=List[Expense],
    summary="Get all expenses",
    status_code=200
)
def expenses(db:Session = Depends(get_db)):
    # querying the database
    expenses=db.query(Expenses).all()
    return expenses

@expenses_router.get("/{userId}",
    tags=["EXPENSES"],
    # response_model=ExpenseInDb,
    summary="Get a single user's expense items basket",
    status_code=200
)
def oneexpense(userId:int,db:Session = Depends(get_db)):
    # querying the database
    item= db.query(Expenses).filter(Expenses.user_id==userId).first()
    user= db.query(User).filter(User.id==userId).first()
    if not user:
        raise HTTPException(status_code=404,detail=f"Sorry user ID {userId} does not exist") 
    if not item:
        raise HTTPException(status_code=404,detail=f"Sorry user {user.first_name} has not yet recorded any expenses") 
    return item

@expenses_router.post("",
    tags=["EXPENSES"],
    response_model=Dict[str,str],
    summary="Add an expense (NOTE: when using this endpoint, just enter the cost of one single expense even if you have more than one quantity of a given expense item)",
    status_code=200
)
def addExpense(payload:CreateExpense, db:Session = Depends(get_db)):
    # querying the database
    item=db.query(Expenses).filter(Expenses.expense == payload.expense).first()        
    user=db.query(User).filter(User.id == payload.userId).first()    
    if not user :
        raise HTTPException(status_code=404,detail=f"Sorry, no such user exist")    
    if item:
        raise HTTPException(status_code=404,detail=f"Sorry, expense {payload.expense} already exist")                   
    coast=payload.quantity*payload.cost
    expense:CreateExpense = Expenses(user_id=payload.userId,expense=payload.expense,quantity=payload.quantity,cost=coast)
    db.add(expense)
    db.commit()
    return {"Message":f"{payload.expense} of quantity {payload.quantity} is now in record"}

@expenses_router.put("/{expenseId}",
    tags=["EXPENSES"],
    response_model=Dict[str,str],
    summary="Edit the details of an expense item from your expense items basket ",
    status_code=200
)
def putExpense(expenseId:int,payload:ExpensePut ,db:Session = Depends(get_db)):
    # querying the database
    item= db.query(Expenses).filter(Expenses.id==expenseId).first()
    user= db.query(User).filter(User.id==item.user_id).first()
    if not item:
        raise HTTPException(status_code=404,detail=f"Item {expenseId} does not exist in your expense items list") 
    if payload.userID != user.id:
        raise HTTPException(status_code=400,detail=f"Invalid User ID")

    coast=payload.quantity*payload.cost
    item.expense=payload.expense
    item.quantity=payload.quantity
    item.cost=coast
    db.merge(item)
    db.commit()
    return {"Message":f"New Expense name:{payload.expense}, New {payload.expense} quantity:{payload.quantity}, New {payload.expense} cost:{coast}"}

@expenses_router.delete("",
    tags=["EXPENSES"],
    response_model=Dict[str,str],
    summary="Remove an expense ite from your expense items basket",
    status_code=200
)
def deleteExpense(expenseId:int,firstName:str,db:Session = Depends(get_db)):
    # querying the database
    item= db.query(Expenses).filter(Expenses.id==expenseId).first()
    user= db.query(User).filter(User.id==item.user_id).first()
    if not item:
        raise HTTPException(status_code=400,detail="Invalid expense ID!")
    if user.first_name == firstName and item.user_id == user.id:
        db.delete(item)
        db.commit()
        return  {"Message":f"Expense item {item.expense} successfully removed"}
    else:
        raise HTTPException(status_code=404,detail="Invalid entery. Check user details then try again!")
    
    