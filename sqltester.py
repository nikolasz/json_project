import os
import pandas as pd
import pyodbc

# Load JSON file into a pandas DataFrame
df = pd.read_json(r'C:\Users\Nick\Downloads\json_project\conversations.json')

# Read Azure SQL connection details from environment variables
server = 'database6202023.database.windows.net'
database = 'Personal ChatGPT History'
username = "CloudSA70f8406e"
password = os.getenv('AZURE_SQL_PASSWORD')

# Create a connection to Azure SQL server
conn = pyodbc.connect('DRIVER={SQL Server};'
                      f'SERVER={server};'
                      f'DATABASE={database};'
                      f'UID={username};'
                      f'PWD={password}')

# Table name for storing the chat data
table_name = 'chat_data'

# Write data from DataFrame to SQL server
df.to_sql(table_name, conn, if_exists='append', index=False)


import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

# Load JSON file into a pandas DataFrame
df = pd.read_json(r'C:\Users\Nick\Downloads\json_project\conversations.json')

# Read Azure SQL connection details from environment variables
server = 'database6202023.database.windows.net'
database = 'Personal ChatGPT History'
password = os.getenv('AZURE_SQL_PASSWORD')

# Create a SQLAlchemy engine for Azure SQL server
engine = create_engine(f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=SQL+Server')

# Table name for storing the chat data
table_name = 'chat_data'

# Write data from DataFrame to SQL server
df.to_sql(table_name, engine, if_exists='append', index=False)


CREATE TABLE chat_data (
    title NVARCHAR(MAX),
    create_time DATETIME2,
    update_time DATETIME2,
    mapping NVARCHAR(MAX),
    moderation_results NVARCHAR(MAX),
    current_node NVARCHAR(255),
    plugin_ids NVARCHAR(MAX),
    id NVARCHAR(255),
    message NVARCHAR(MAX),
    timestamp DATETIME
)
