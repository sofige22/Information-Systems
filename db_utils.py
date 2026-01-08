import mysql.connector as mdb
from datetime import date

# הגדרות החיבור (במקום אחד מרכזי)
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'passwd': 'root123456',
    'database': 'FLYTAU'
}

def get_connection():
    return mdb.connect(**DB_CONFIG)

def is_manager(uid, pwd):
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Managers WHERE ManagerID = %s AND M_Password = %s", (uid, pwd))
    res = cursor.fetchone()
    con.close()
    return res

def is_customer(email, pwd):
    con = get_connection()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM RegisteredCustomers WHERE RegEmail = %s AND R_Password = %s", (email, pwd))
    res = cursor.fetchone()
    con.close()
    return res

def add_customer(data):
    try:
        con = get_connection()
        cursor = con.cursor()
        sql = """INSERT INTO RegisteredCustomers 
                 (CustomerID, FirstName, LastName, RegEmail, R_Password, Address, PassportNumber, BirthDate, RegistrationDate) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (data['id'], data['f_name'], data['l_name'], data['email'],
                  data['pwd'], data['address'], data['passport'], data['dob'], date.today())
        cursor.execute(sql, values)
        con.commit()
        con.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False