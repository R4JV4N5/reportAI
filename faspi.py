from fastapi import FastAPI
import os
import prompt_data as prd
import modelclass as mc
from fastapi.middleware.cors import CORSMiddleware
import base64
import re

from utils import get_questions,get_answer,base_model,gen_report



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows your front-end to access the back-end
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)





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
      qlist = request.questions_list
      
      quest_object = get_questions(start_date,end_date)
      
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
      if len(final_object) ==7:
        
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
  quest_string = get_questions("","")
  questions_list = quest_string.split(" + ")

  return  mc.questionsResponse(
    message="questions generated sucessfully",
    status=200,
    data=questions_list
  )
      
# @app.api_route("/generate_report/", methods=["GET", "POST"], response_model=mc.ReportResponse)
# async def generate_report(request: mc.ReportRequest):
  # print(request)
  # return {
  #                   "message": "questions generated successfully",
  #                   "status": "success",
  #                   "data": {"base_string": f"{request.end_date}"}
  #               }