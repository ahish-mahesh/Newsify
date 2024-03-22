import sqlite3

conn = sqlite3.connect('newsifyDb.db')
print("Opened database successfully")

conn.execute('''CREATE TABLE USERS
         (USERNAME           TEXT    NOT NULL,
         PASSWORD            TEXT     NOT NULL,
         COUNTRY             TEXT     NOT NULL,
         TAGS                JSON);''')
print("Table created successfully")

conn.close()