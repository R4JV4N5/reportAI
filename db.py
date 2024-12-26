from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()


username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')  # Update the host to allow Docker to access local machine
database = os.getenv('DB')

# Construct the connection string
connection_string = f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'

# Create an engine
engine = create_engine(connection_string)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test the connection
try:
    with engine.connect() as connection:
        result = connection.execute(text("select count(UserID) from users"))  # Use `text` for raw SQL queries
        print("Connection successful:", result.fetchall())
except Exception as e:
    print("Connection failed:", str(e))
