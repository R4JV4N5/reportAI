from gen_report import create_report_template
import json
import sqlparse
from groq import Groq
import sqlite3
import pandas as pd
import os
import prompt_data as prd
import re



from dotenv import load_dotenv
load_dotenv()



MODEL_NAME = "llama3-70b-8192"

# Get the Groq API key and create a Groq client
groq_api_key = os.getenv('groq_api_key')



with open('prompts/base_prompt.txt', 'r') as file:
  base_prompt = file.read()

client = Groq(api_key=groq_api_key)


def base_model(ast_prompt,prompt):
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
    
  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "user",
            "content": """Based on the db information Generate questions and sqlite3 queries based on the provided table columns information for report generation where payment dates are between {start_date} and {end_date}: {db_columns_info}.
            
            Strict rules for questions :
          question 1 based on Overall Payment Performance
          question 2 based on Payment Trends Across Batches and Courses
          question 3 based on Comparison of Payment Modes
          question 4 based on Installment Payment Analysis
          question 5 based on Revenue Projections Based on Payment Trends
          question 6 based on Semester-Wise Payment Overview
          question 7 based on Conclusion and Future Outlook
             
             number of questions : 7
             strict output format :  [{{"title:<>,question_number:<> , question:<> , sql_query: <>}}] 
             Use Where only when necessary. avoid using assumed values in where conditions
             Ensure that the questions are based on the provided table columns information and Queries are valid for SQLite3
             
             Queries is must for every question
             """.format(db_columns_info = prd.db_columns_info,start_date=start_date,end_date=end_date)
        },
        {
            "role": "assistant",
            "content": "```json"
        }
    ],
  stop="```",
    model='llama3-70b-8192')
  print("genertating questions")
  op = chat_completion.choices[0].message.content
  # if 'question_number:' in op and 'question:' in op and 'sql_query:' in op:
  # print(op)
  questions = json.loads(op)
  return questions

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
  
  
    df = pd.read_csv('data/jain_university_data.csv')

    # Connect to an SQLite database (in-memory or file-based)
      # Use ':memory:' for an in-memory database or provide a filename   
    
    conn = sqlite3.connect('database/temp_database.db')
    
    # Write the DataFrame to a new table in the SQLite database
    df.to_sql('university_data', conn, index=False, if_exists='replace')  # Replace the table if it already exists

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

    In a few sentences, summarize the data in the table as it pertains to the original user question. Avoid qualifiers like "based on the data" and do not comment on the structure or metadata of the table itself in 50 words.
    Avoid using special Characters . use indian currency
  '''.format(user_question = user_question, df = df)
    print("genertating sql summary")

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

def get_answer(question_json): 
  # user_question = input("Ask a question: ")
  if question_json:
      # Generate the full prompt for the AI
      # full_prompt = base_prompt.format(user_question=user_question)

      # Get the AI's response. Call with '{"type": "json_object"}' to use JSON mode
      # llm_response = chat_with_groq(client, full_prompt, MODEL_NAME, {"type": "json_object"})

      
      if 'sql_query' in question_json:
          question = question_json['question']
          sql_query = question_json['sql_query']
          results_df = execute_sql_query(sql_query)

          formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

          # print("```sql\n" + formatted_sql_query + "\n```")
          # print(results_df.to_markdown(index=False))
          print("genertating sql answer")

          summarization = get_summarization(client,question,results_df,MODEL_NAME)
          question_json['data'] = results_df.to_json(orient='records')
          question_json['summary'] = summarization
          return question_json
        
      else:
          print("ERROR:", 'Could not generate valid SQL for this question')
          return "no query found"# print(result_json['error'])


def gen_report(report_summary):
  
  report_contents = []
  for i in prd.prompt_list:
    contents_output = base_model(prd.ast_report_prompt, f"{i.format(report_summary=report_summary)} in 40 words.Generate without any introductory phrases or contextual framing such as 'Here is an analysis of the overall financial performance.It must be stakeholders friendly. it should not include special symbols like * .Generate a concise and accurate response")
    report_contents.append(contents_output)
    
  if len(report_contents) == 7:
    create_report_template(report_contents)
    return True 
  else:
    return False     

