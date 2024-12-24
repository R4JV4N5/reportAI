from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


username = 'root'
password = 'root'
host = 'localhost'
database = 'reportai_database'

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
# try:
#     with engine.connect() as connection:
#         result = connection.execute(text("select * from users"))  # Use `text` for raw SQL queries
#         print("Connection successful:", result.fetchall())
# except Exception as e:
#     print("Connection failed:", str(e))
