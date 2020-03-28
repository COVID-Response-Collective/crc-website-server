import pg8000
import json
import enum
from datetime import datetime

class Role(enum.Enum):
    COMM = 'COMM MEMBER'
    EMAUTH = 'EM AUTH'

class Status(enum.Enum):
    OPEN = 'OPEN'
    FULFILLED = 'FULFILLED'

class Database:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.conn = pg8000.connect(user="postgres", password=config['postgres_pw'])
        self.cursor = self.conn.cursor()

def initDB():
    db = Database()
    db.cursor.execute("DROP TABLE IF EXISTS requests")
    db.cursor.execute("CREATE TYPE role_type AS ENUM ('COMM MEMBER', 'EM AUTH')")
    db.cursor.execute("CREATE TYPE status_type AS ENUM ('OPEN', 'FULFILLED')")
    db.cursor.execute("SET timezone = 'America/Los_Angeles'")
    db.cursor.execute("CREATE TABLE requests (rID SERIAL NOT NULL, name VARCHAR(64) NOT NULL, role role_type NOT NULL, email VARCHAR(64), phone VARCHAR(32), request VARCHAR(600), status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateFulfilled TIMESTAMPTZ NOT NULL, PRIMARY KEY (rID))")
    db.conn.commit()
    return db

def test():
    db = Database()
    
    db.cursor.execute("DROP TABLE IF EXISTS test")
    db.cursor.execute("SET timezone = 'America/Los_Angeles'")
    db.cursor.execute("CREATE TABLE test (rID SERIAL NOT NULL, name VARCHAR(64) NOT NULL, role role_type NOT NULL, email VARCHAR(64), phone VARCHAR(32), request VARCHAR(600), status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateFulfilled TIMESTAMPTZ, PRIMARY KEY (rID))")
    db.conn.commit()
    
    name = 'test'
    roleValue = 1
    email = 'test'
    phoneValue = '123'
    req = 'request'
    
    if email == '':
        email = None
    if phoneValue == '':
        phone = None
    else:
        phone = phoneValue
    if roleValue == 1:
        role = Role.COMM
    else:
        role = Role.EMAUTH
    status = Status.OPEN
    dateOpened = datetime.now()

    db = Database()
    db.cursor.execute("INSERT INTO test (name, role, email, phone, request, status, dateOpened) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING rID", (name, role, email, phone, req, status, dateOpened))
    db.conn.commit()
        
    results = db.cursor.fetchall()
    for row in results:
        print("New request ID: %s" % (row))
        rID = row.pop()

    db = Database()
    db.cursor.execute("UPDATE test SET status = %s, dateFulfilled = %s WHERE rID = %s", (Status.FULFILLED, datetime.now(), rID))
    db.conn.commit()

    db.cursor.execute("SELECT * from test")
    db.conn.commit()

    results = db.cursor.fetchall()
    for row in results:
        print(row)

