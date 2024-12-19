from fastapi import FastAPI, HTTPException, Depends, Request
import os
import modelclass as mc
from fastapi.middleware.cors import CORSMiddleware
import json
from utils import get_questions,get_answer,base_model
from db import get_db

from auth import authenticate_user,sessions,create_session,pwd_context
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from modelclass import UserDB,ReportDB,UserCreate,UserLoginModel,UserIDRequest,LogoutRequestModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows your front-end to access the back-end
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


print(sessions)

@app.api_route("/generate_report/", methods=["POST"], response_model=mc.ReportResponse)
async def generate_report(request: mc.ReportRequest):
    file_path = 'report/reportai.pdf'

# Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
        print(f"{file_path} has been deleted.")
    else:
        print(f"The file {file_path} does not exist.")
  
    if(request):
    # Example: Access specific keys if they exist
      start_date = request.start_date
      end_date = request.end_date
      qlist = request.qlist
      
      
      quest_object = get_questions(start_date,end_date,qlist)
      
      final_object = []
      
      if quest_object != "quit":
        if  len(quest_object)>0:
          for i in quest_object:
            print(i)
            answer_object = get_answer(i)
            final_object.append(answer_object)
      else:
        return mc.ReportResponse(
                message="error generating questions retry",
                status=500,
                # data={"base_string": pdf_data}
                data="No questions"
                  )
      if len(final_object) > 0:
        print(f'\n\n\n{final_object}')
        return mc.ReportResponse(
                message="output generated succesfully",
                status=200,
                # data={"base_string": pdf_data}
                data= final_object )
    else:
      return mc.ReportResponse(
                message="invalid request",
                status=500,
                # data={"base_string": pdf_data}
                data= "")
          
  
@app.api_route("/suggest_questions/",methods=["GET"],response_model=mc.questionsResponse)  
async def suggest_questions():
  quest_string = base_model()
  # questions_list = quest_string.split(" + ")
  question_list = json.loads(quest_string)
  print(quest_string)
  return  mc.questionsResponse(
    message="questions generated sucessfully",
    status=200,
    data=question_list
  )
  
  # endpoints for user auth
  
@app.api_route("/save_report/", methods=["POST"])
async def save_report(request: mc.saveReportRequest, db: Session = Depends(get_db)):
    try:
        if request:
            new_report = ReportDB(
                UserID=request.UserID,
                Title=request.Title,
                Description=request.Description,
                Report_data=request.ReportData
            )
            db.add(new_report)
            db.commit()
            db.refresh(new_report)
            return {
                "status": 200,
                "isSucess": True,
                "message": "Report saved successfully",
            }
    except Exception as e:
        # Log the error (optional)
        return {
            "status": 500,
            "isSucess": False,
            "message": f"An error occurred: {str(e)}",
        }


@app.api_route("/get_reports", methods=["POST"])
async def get_reports(user: UserIDRequest, db: Session = Depends(get_db)):
    print(user.UserID)
    try:
        # Query to get all reports for the given UserID
        if user:
            
            reports = db.query(ReportDB).filter(ReportDB.UserID == user.UserID).all()

        # Check if reports exist
            if reports:
                # Format the response with the reports data
                return {
                    "status": 200,
                    "isSuccess": True,
                    "message": "Reports retrieved successfully",
                    "data": [  # Convert report objects to dictionaries or your response model
                        {   "ReportID":report.ID,
                            "Title": report.Title,
                            "Description": report.Description,
                            "ReportData": report.Report_data,
                        }
                        for report in reports
                    ],
                }
            else:
                return {
                    "status": 404,
                    "isSuccess": False,
                    "message": "No reports found for the given UserID",
                }
    except Exception as e:
        # Handle unexpected errors
        return {
            "status": 500,
            "isSuccess": False,
            "message": f"An error occurred: {str(e)}",
        }


  
# user auth

@app.post("/login")
async def login(user:UserLoginModel, db: Session = Depends(get_db)):
    user_obj = authenticate_user(db, user.identifier,user.password)
    if not user_obj:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    session_id = create_session(user_obj)
    existing_user = db.query(UserDB).filter((UserDB.Username == user.identifier) | (UserDB.Email == user.identifier)).first()
    if existing_user:
      userId = existing_user.UserID
    response = JSONResponse({"status": 200,"isSucess":True,"message": "Login successful","UserId":userId ,"SessionId":session_id})
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    print(response)
    return response


@app.post("/logout")
async def logout(request:LogoutRequestModel):
    print(request)
    print(sessions)
    session_id = request.SessionId
    if session_id in sessions:
        del sessions[session_id]
        response = JSONResponse({"status": 200,"isSucess":True,"message": "Logged out successfully"})
        response.delete_cookie("session_id")
        return response
    raise HTTPException(status_code=401, detail="Invalid session or already logged out")


@app.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(UserDB).filter(
        (UserDB.Username == user.username) | (UserDB.Email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with the same username or email already exists")
    
    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    
    # Create a new user
    new_user = UserDB(Username=user.username, Email=user.email, Password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": 200,"isSucess":True,"message": "User registered successfully",}


