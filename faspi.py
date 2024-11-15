from fastapi import FastAPI ,Request
import os
from groq import Groq
import json
import sqlparse
import numpy as np
import pandas as pd
import sqlite3
from dotenv import load_dotenv
import prompt_data as prd
import modelclass as mc
from fastapi.middleware.cors import CORSMiddleware
import base64
import re
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows your front-end to access the back-end
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

MODEL_NAME = "llama3-70b-8192"


# Get the Groq API key and create a Groq client
groq_api_key = os.getenv('groq_api_key')

client = Groq(api_key=groq_api_key)
# Load the base prompt
with open('prompts/base_prompt.txt', 'r') as file:
  base_prompt = file.read()

def base_model(ast_prompt,prompt):
  client = Groq(api_key=groq_api_key)

  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "assistant",
            "content": f"{ast_prompt} ",
        },
        {
            "role": "user",
            "content": f""" {prompt} """,
        }
    ],
    model=MODEL_NAME,
    stream=False,)

  return chat_completion.choices[0].message.content
  
def get_questions(start_date, end_date):
  client = Groq(api_key=groq_api_key)

  if start_date == "" and end_date =="":
    _model = 'llama3-8b-8192'
    count = 3
    suggest_questions_prompt = ""
  else:
     _model = 'llama3-70b-8192'
     count=5
     suggest_questions_prompt = f"These questions should be designed to facilitate the creation of a detailed company report for the period between {start_date} and {end_date}."

  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "assistant",
            "content": f"{prd.questions_prompt}",
        },
        {
            "role": "user",
            "content": """Generate a set of {count} questions based on the provided table columns information: {db_columns_info}.
            
            questions should be generated in such a way that it may covers these points :
            1. Overall Financial Performance
            2. Revenue Breakdown
            3. Expense Analysis
            4. Profit Margins
            5. Cash Flow
            6. Key Financial Ratios
            7. Conclusion and Outlook
            
            {suggest_questions_prompt}
                            Format the output strictly as follows:
                            question1 + question2 + question3 + ... + question{count}.

                            Each question should begin with a question word (e.g., What, How, When, etc.).
                            Do not include any introductory phrases like "Here are..." or similar statements.

                            Expected Output Example:
                            What is the user's primary email address? + How many different usernames has the user had over time? + What is the last login date for this user?

            """.format(count=count,db_columns_info = prd.db_columns_info,suggest_questions_prompt=suggest_questions_prompt),
        }
    ],
    model="llama3-8b-8192",
    stream=False,)
  print("genertating questions")

  return chat_completion.choices[0].message.content

def chat_with_groq(client, prompt, model, response_format):
  completion = client.chat.completions.create(
  model=model,
  messages=[
      {
          "role": "user",
          "content": prompt
      }
  ],
  response_format=response_format
  )

  return completion.choices[0].message.content

def execute_sql_query(query):
    df = pd.read_csv('data/Financials.csv')

    # Connect to an SQLite database (in-memory or file-based)
      # Use ':memory:' for an in-memory database or provide a filename   
    
    conn = sqlite3.connect('database/Finance_database.db')
    
    # Write the DataFrame to a new table in the SQLite database
    df.to_sql('finance_data', conn, index=False, if_exists='replace')  # Replace the table if it already exists

    # Execute the query and fetch the result
    query_result = pd.read_sql(query, conn)

    # Close the connection
    conn.close()

    return query_result

def get_summarization(client, user_question, df, model):
    """
    This function generates a summarization prompt based on the user's question and the resulting data. 
    It then sends this summarization prompt to the Groq API and retrieves the AI's response.

    Parameters:
    client (Groqcloud): The Groq API client.
    user_question (str): The user's question.
    df (DataFrame): The DataFrame resulting from the SQL query.
    model (str): The AI model to use for the response.

    Returns:
    str: The content of the AI's response to the summarization prompt.
    """
    prompt = '''
      A user asked the following question pertaining to local database tables:
    
      {user_question}
    
      To answer the question, a dataframe was returned:
    
      Dataframe:
      {df}

    In a few sentences, summarize the data in the table as it pertains to the original user question. Avoid qualifiers like "based on the data" and do not comment on the structure or metadata of the table itself
  '''.format(user_question = user_question, df = df)
    print("genertating sql summary")

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

def get_answer(user_question): 
  # user_question = input("Ask a question: ")
  if user_question:
      # Generate the full prompt for the AI
      full_prompt = base_prompt.format(user_question=user_question)

      # Get the AI's response. Call with '{"type": "json_object"}' to use JSON mode
      llm_response = chat_with_groq(client, full_prompt, MODEL_NAME, {"type": "json_object"})

      result_json = json.loads(llm_response)
      if 'sql' in result_json:
          sql_query = result_json['sql']
          results_df = execute_sql_query(sql_query)

          formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

          # print("```sql\n" + formatted_sql_query + "\n```")
          # print(results_df.to_markdown(index=False))
          print("genertating sql answer")

          summarization = get_summarization(client,user_question,results_df,MODEL_NAME)
          return summarization
        
      elif 'error' in result_json:
          
          print("ERROR:", 'Could not generate valid SQL for this question')
          # print(result_json['error'])


def extract_code(input_string):
    # Regex to match the content between triple backticks
    code_pattern = r'```(.*?)```'
    
    # Find all matches (non-greedy match to get content inside backticks)
    code = re.findall(code_pattern, input_string, flags=re.DOTALL)
    
    # If code is found, remove the word 'python' (case-insensitive) from the extracted code
    if code:
        code = code[0]
        # Remove the word 'python' (case-insensitive)
        code = re.sub(r'\bpython\b', '', code, flags=re.IGNORECASE)
    
    # Return the cleaned code or an empty string if no code is found
    return code if code else ""

def gen_report(report_summary):
  
  success = True
  retry_count = 0
  max_retries = 5

  while success and retry_count < max_retries:  
    error = []
    report_code = base_model(prd.report_code_generation, prd.user_prompt.format(report_summary=report_summary,error = error,code_template = prd.code_template))

    cde = extract_code(report_code)
    try:
        print("genertating report")
        exec(cde)
        success = False
        return 1
         
    except Exception as e:
        retry_count += 1
        print(f"Attempt {retry_count} failed with error: {e}")
        error.append(e)
        if retry_count >= max_retries:
          return 0
          
  




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
      
      questions_string = get_questions(start_date ,end_date)
      questions_list = questions_string.split(" + ")
      
      if len(qlist)!=0:
         questions_list.extend(qlist)
         print(questions_list)
      print(questions_list)
      QA = {}
      
      for i in questions_list:
        try:
          answer  = get_answer(i)
          QA[i] = answer
        except Exception as e:
  #         # Optionally log the error message: print(f"Error: {e}")
          continue
      qa_text = "\n".join([f"{question}: {answer}" for question, answer in QA.items()])

      report_summary = base_model(prd.ast_sum_prompt,prd.report_summary_prompt.format(qa_text=qa_text))
    
      val = gen_report(report_summary)
    # report_code = base_model(prd.report_code_generation)
    
    if val == 1:
      pdf_path = "report/reportai.pdf"
    
      if os.path.exists(pdf_path):
          # Open the PDF and encode it to base64
          with open(pdf_path, "rb") as pdf_file:
              print('in pdf base')
              pdf_data = str(base64.b64encode(pdf_file.read()).decode('utf-8')) 
              
          print('before returning success\n\n')       
          return mc.ReportResponse(
                message="report generated sucessfully",
                status=200,
                # data={"base_string": pdf_data}
                data=pdf_data
            )
    elif val!=1:
      print('before returning failure \n\n')
      return mc.ReportResponse(
        message="error generating report",
        status=404,
        # data={"base_string": "no data"}
        data="no data"
    )
      

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