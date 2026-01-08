import mysql.connector as mdb
import pandas as pd
import plotly.graph_objects as go

# בתוך הפונקציה ב-main.py:
con = mdb.connect(host='127.0.0.1', user='root', passwd='root123456', database='FLYTAU') #
cursor = con.cursor() #
cursor.execute("SHOW DATABASES")
# running SQL #retrieve all records
print(cursor.fetchall())