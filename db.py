from sqlalchemy import create_engine


# Define database connection parameters
username = 'root'
password = 'root'
host = 'localhost'
database = 'reportai_database'

# Construct the connection string
connection_string = f'mysql+mysqlconnector://{username}:{password}@{host}/{database}'

    # Create the engine
engine = create_engine(connection_string)