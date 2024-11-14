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

  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "assistant",
            "content": f"{prd.questions_prompt}",
        },
        {
            "role": "user",
            "content": f"""Based on the table columns provided— \n{prd.db_columns_info}\n —generate only 5 questions that will help in analyzing and creating a comprehensive company report dated between {start_date} and {end_date}.   
            strictly format : (example : question1 + question2....)

             Reminder !! ONLY Questions , do not generate anything else
            """,
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
    
    conn = sqlite3.connect('Finance_database.db')
    
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
    report_code = base_model(prd.report_code_generation, prd.user_prompt.format(report_summary=report_summary,error = error))

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
          
  




@app.api_route("/generate_report/", methods=["GET", "POST"], response_model=mc.ReportResponse)
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
      
      questions_string = get_questions(start_date ,end_date)
      questions_list = questions_string.split(" + ")
      
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
              pdf_data = base64.b64encode(pdf_file.read()).decode('utf-8') 
              
          print('before returning success\n\n')       
          return mc.ReportResponse(
                message="report generated sucessfully",
                status=200,
                data={"base_string": pdf_data}
            )
    elif val!=1:
      print('before returning failure \n\n')
      return mc.ReportResponse(
        message="error generating report",
        status=404,
        data={"base_string": "no data"}
    )
      
      
      
# @app.api_route("/generate_report/", methods=["GET", "POST"], response_model=mc.ReportResponse)
# async def generate_report(request: mc.ReportRequest):
  # print(request)
  # return {
  #                   "message": "questions generated successfully",
  #                   "status": "success",
  #                   "data": {"base_string": f"{request.end_date}"}
  #               }