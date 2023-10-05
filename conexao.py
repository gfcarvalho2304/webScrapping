import pyodbc
import os

server_name = os.environ.get('SQL_SERVER_NAME')
database_name = os.environ.get('SQL_DATABASE_NAME')
username = os.environ.get('SQL_USERNAME')
password = os.environ.get('SQL_PASSWORD')

conn = pyodbc.connect(
    f'DRIVER=SQL Server;SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
)
