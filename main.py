import os
from groq import Groq
import json
import sqlparse
import numpy as np
import pandas as pd
import sqlite3
from dotenv import load_dotenv
import prompt_data as prd
load_dotenv()

MODEL_NAME = "llama3-70b-8192"



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

    In a few sentences, summarize the data in the table as it pertains to the original user question. Avoid qualifiers like "based on the data" and do not comment on the structure or metadata of the table itself , try to include numerical information too
  '''.format(user_question = user_question, df = df)

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

# Get the Groq API key and create a Groq client
groq_api_key = os.getenv('groq_api_key')

client = Groq(api_key=groq_api_key)
# Load the base prompt
with open('prompts/base_prompt.txt', 'r') as file:
  base_prompt = file.read()

# while True:
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

          summarization = get_summarization(client,user_question,results_df,MODEL_NAME)
          print(f"question:{user_question}\n\nAnser:{summarization}\n\n\n")
      elif 'error' in result_json:
          
          print("ERROR:", 'Could not generate valid SQL for this question')
          # print(result_json['error'])





def get_questions():
  client = Groq(api_key=groq_api_key)

  chat_completion = client.chat.completions.create(
  messages=[
        {
            "role": "assistant",
            "content": f"{prd.questions_prompt}",
        },
        {
            "role": "user",
            "content": f"""Based on the table columns provided— \n{prd.db_columns_info}\n —generate only 5 questions that will help in analyzing and creating a comprehensive company report.   
            strictly format : (example : question1 + question2....)

            Reminder !! ONLY Questions , do not generate anything else
            """,
        }
    ],
    model="llama3-8b-8192",
    stream=False,)

  return chat_completion.choices[0].message.content

quest = get_questions()

questions_list = quest.split(" + ")

for question in questions_list:
    print(question)

# for i in questions_list:
#     try:
#         get_answer(i)
#     except Exception as e:
#         # Optionally log the error message: print(f"Error: {e}")
#         continue

