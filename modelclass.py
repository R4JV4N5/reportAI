from pydantic import BaseModel,EmailStr

class ReportRequest(BaseModel):
    start_date: str
    end_date: str
    qlist:list


class ReportResponse(BaseModel):
    message: str
    status: int
    data: list 

class questionsResponse(BaseModel):
    message: str
    status: int
    data: list[str] | list[dict]
    
    
# user models    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  
    
class UserLoginModel(BaseModel):
    identifier:str #can check email as well as password
    password:str  


# db models

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)