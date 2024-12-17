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
    
 
#  report model
class UserIDRequest(BaseModel):
    userID: int
    
class saveReportRequest(BaseModel):
    UserID: int
    Title:str
    Description:str
    ReportData: str
    
    

    
# user models    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str  
    
class UserLoginModel(BaseModel):
    identifier:str #can check email as well as password
    password:str  


# db models

from sqlalchemy import Column, String, Integer,LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserDB(Base):
    __tablename__ = "users"
    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Username = Column(String(50), unique=True, nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    
class ReportDB(Base):
    __tablename__ = "report_data"
    ID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    UserID = Column(Integer, primary_key=True, index=True)
    Title = Column(String(50), unique=True, nullable=False)
    Description = Column(String(100), unique=True, nullable=False)
    Report_data = Column(LargeBinary, nullable=False)