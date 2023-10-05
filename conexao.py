import pyodbc

server_name ='DESKTOP-ADV3BR6'
database_name = 'Brasileirao'
username ='sa'
password ='bAran321!'

conn = pyodbc.connect(
    f'DRIVER=SQL Server;SERVER={server_name};DATABASE={database_name};UID={username};PWD={password}'
)
"""
cursor = conn.cursor()
cursor.execute("SELECT * from artilharia")
resultado = cursor.fetchone()
print(resultado)
cursor.close()
conn.close()
"""