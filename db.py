import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL'] # ----- DATABASE_URL saved on heroku as environment variable

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

def db_retrieve(): # retrieves which week is to be updated
    try:
        cur.execute("CREATE TABLE week (number integer); INSERT INTO week (number) VALUES (1);")
        cur.execute("SELECT number FROM week;")
    except:
        cur.execute("ROLLBACK")
        cur.execute("SELECT number FROM week;")
    conn.commit()

    number = cur.fetchone()[0]
    print(f"Now editing: {number}")
    return(number)

def db_update(week_no):
    try:
        cur.execute(f"UPDATE week SET number={week_no};")
        cur.execute("SELECT number FROM week;")
        number = cur.fetchone()[0]
    except:
        cur.execute("ROLLBACK")
        cur.execute("SELECT number FROM week;")
        number = cur.fetchone()[0]
    conn.commit()

    print(f"Next week: {number} (value in db)")