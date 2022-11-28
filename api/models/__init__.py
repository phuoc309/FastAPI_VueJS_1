import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT # <-- ADD THIS LINE
from api.models.database import db, Book, Categories, Account, Borrow

conn = psycopg2.connect(host='localhost', user='postgres', password='postgres')
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
try:
    conn.cursor().execute('CREATE DATABASE library')
    conn.close()
    db.connect()
    db.create_tables([Book, Categories, Account, Borrow])
    print("Database is created")
except:
    print("Database is already created")

conn.close()