from fastapi import APIRouter,Depends,HTTPException
from typing import List,Dict,Generator
from db.session import SessionLocal
from schema import  UserInfo,CreateUser,UserPut,UserInDb
from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.user import User

def get_db() -> Generator:
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

user_router=APIRouter()

#  My Endpints:
@user_router.get("/",
    tags=["USERS"],
    response_model=list[UserInfo],
    summary="all users",
    status_code=200
)
def users(db:Session = Depends(get_db)):
    # querying the database  
    users=db.query(User).all()  
    return users

@user_router.get("/{emailaddress}",
    tags=["USERS"],
    response_model=UserInfo,
    summary="A single users",
    status_code=200
)
def oneUser(emailaddress:str,db:Session =Depends(get_db)):
    you=db.query(User).filter(User.email==emailaddress).first()
    if not you:
        raise HTTPException(status_code=400,detail=f"Sorry,the email {emailaddress} doesn't exist")
    return you

@user_router.post("/",
    tags=["USERS"],
    response_model=UserInfo,
    summary="Add a  User",
    status_code=200
)
def addUser(payload:CreateUser,db:Session = Depends(get_db)):
    # check if the email exists
    email=db.query(User).filter(User.email == payload.email).first()
    if email:
        raise HTTPException(status_code=400,detail=f"{payload.email},is already taken")    
    print("payload",payload.dict())
    print("payload type",type(payload))
    server_default=func.now()
    now=server_default
    res:UserInDb = User(first_name=payload.first_name,last_name=payload.last_name,email=payload.email,date=now)
    db.add(res)
    db.commit()
    return res    

@user_router.put("/{userID}",
    tags=["USERS"],
    response_model=UserInfo,
    summary="Update User's details",
    status_code=200
)
def oneUser(userID:int,payload:UserPut,db:Session = Depends(get_db)):
    you=db.query(User).filter(User.id==userID).first()
    if not you:
        raise HTTPException(status_code=400,detail="Invalid user ID!")
    you.email=payload.email
    you.first_name=payload.first_name
    you.last_name=payload.last_name
    db.merge(you)
    db.commit()
    return you    

@user_router.delete("/}",
tags=["USERS"],
response_model= Dict[str,str],
summary="delete a specific user",
status_code=200,
)
def delete_user(userID:int,email:str,db:Session = (Depends(get_db))):
    you=db.query(User).filter(User.id==userID).first()
    if not you and User.email!=email:
        raise HTTPException(status_code=400,detail="Invalid entery!")
    if you.email==email:
        db.delete(you)
        db.commit()
        return {"Message":f"User {you.first_name} successfully removed"}  
    else:
        raise HTTPException(status_code=400,detail="Invalid entery(email address)!")  