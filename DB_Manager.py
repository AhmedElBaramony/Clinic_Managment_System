import pypyodbc as odbc
from datetime import datetime

def calculate_age(birth_date_str):

    # Parse the birthdate string into a datetime object
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")

    # Get the current date
    current_date = datetime.now()

    # Calculate the difference in years
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))

    return age

def connect_to_database(driver, server, database):
    connection_string = f'''
        DRIVER={{{driver}}};
        SERVER={server};
        DATABASE={database};
        Trust_Connection=True;
    '''
    connection = odbc.connect(connection_string)
    inner_cursor = connection.cursor()
    return inner_cursor, connection


def execute_query(cursor, query):
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows


def execute_procedure(cursor, procedure):
    cursor.execute(procedure)
    rows = cursor.fetchall()
    return rows

def execute_insert_procedure(cursor, conn, procedure):
    cursor.execute(procedure)
    conn.commit()

#cursor, conn = connect_to_database('SQL Server', 'LAPTOP-QQTU5VR3\\MSSQLSERVER22', 'Clinical_Management_System')
