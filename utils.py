# from gen_report import create_report_template
import json
import sqlparse
from groq import Groq
import pandas as pd
import os
import prompt_data as prd
from db import engine


from dotenv import load_dotenv
load_dotenv()



MODEL_NAME = "llama3-70b-8192"

# Get the Groq API key and create a Groq client
groq_api_key = os.getenv('groq_api_key')



with open('prompts/base_prompt.txt', 'r') as file:
  base_prompt = file.read()

client = Groq(api_key=groq_api_key)
  
def get_questions(start_date, end_date ,qlist):
 
  user_question = '\n'.join(qlist)
  if len(start_date) >0 and len(end_date) > 0:
    date_string = "where payment dates are between {start_date} and {end_date}".format(start_date=start_date,end_date=end_date)
  else:
    date_string = ""
  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "user",
            "content": """Based on the db information Generate questions and sqlite3 queries based on the provided table columns information for report generation {date_string} : {db_columns_info}.
            

            generate questions and queries for the following topic : {user_question},
            user proper date formats suitable for queries 
            Avoid generating similar questions and provide appropriate report section titles .
             strict output format :  [{{"title:<>,question_number:<> , question:<> , sql_query: <>}}] 
             Use Where only when necessary. avoid using assumed values in where conditions
             Ensure that the questions are based on the provided table columns information and Queries are valid for SQLite3 and are suitable for report generation
             
             
             
             Queries is must for every question
             """.format(db_columns_info = prd.db_columns_info,date_string= date_string,user_question=user_question)
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
  max_tokens=1024,
  messages=[
      {
          "role": "user",
          "content": prompt
      }
  ],
  response_format=response_format,
  
  )

  return completion.choices[0].message.content

def execute_sql_query(query):
  
    # Write the DataFrame to a new table in the SQLite database
    query_result = pd.read_sql(query, engine)

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
    Avoid using special Characters . Use units in amounts like 12000 rupees or 10 cr or 1 lakhs
  '''.format(user_question = user_question, df = df)
    print("genertating sql summary")

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

def get_answer(question_json): 
  # user_question = input("Ask a question: ")
  if question_json:

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


def base_model():
  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "user",
            "content": """Based on the db information Generate questions based on the provided table columns information for report generation : {db_columns_info}.
            
            use proper dates for questions 
            Avoid generating similar questions.
            Number of questions : 15
             strict output format :  [{{"question_number:<> , question:<> }}] 
             
             examples of questions:
             What is the total revenue collected for each course?
             How is the revenue distributed across different batches?
             What is the payment mode distribution for all transactions?
             
             Use Where only when necessary. avoid using assumed values in where conditions
             Ensure that the questions are based on the provided table columns information and are suitable for report generation
             
             """.format(db_columns_info = prd.db_columns_info)
        },
        {
            "role": "assistant",
            "content": "```json"
        }
    ],
  stop="```",
  max_tokens=1024,
    model='llama3-70b-8192')

  return chat_completion.choices[0].message.content