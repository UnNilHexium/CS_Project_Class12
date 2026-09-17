import mysql.connector as m

try:
    gamer_data = m.connect(host="localhost", user="root", password="")
except Exception:
    print("There was an error connecting to the database.")
    host = input("Please enter host: ")
    user = input("Please enter user: ")
    password = input("Please enter password: ")
    gamer_data = m.connect(host=host, user=user, password=password)

db_cur = gamer_data.cursor()

try:
    db_cur.execute("USE gamer_data")
except Exception:
    print("DB does not exist. Creating database...")
    db_cur.execute("CREATE DATABASE gamer_data")
    db_cur.execute("USE gamer_data") 


