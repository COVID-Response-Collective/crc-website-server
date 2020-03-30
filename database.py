import pg8000
import json
import enum
from datetime import datetime

class Role(enum.Enum):
    COMM = 'COMM MEMBER'
    EMAUTH = 'EM AUTH'

class Status(enum.Enum):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN PROGRESS'
    FULFILLED = 'FULFILLED'

class Region(enum.Enum):
    CORVALLIS = 'ALBANY CORVALLIS PHILOMATH'
    PORTLAND = 'PORTLAND METRO'
    EUGENE = 'EUGENE'
    SALEM = 'SALEM'
    DESCHUTES = 'DESCHUTES COUNTY'
    WASCO_HOOD = 'WASCO HOOD RIVER COUNTY'
    POLK_YAMHILL = 'POLK YAMHILL COUNTY'
    MEDFORD = 'MEDFORD ASHLAND'
    KING = 'KING COUNTY'
    SPOKANE = 'SPOKANE'
    WALLOWA = 'WALLOWA'

class RequestType(enum.Enum):
    GROCERY = 'GROCERY'
    PROJECT = 'PROJECT'
    FUNDS = 'FUNDS'
    IN_HOME = 'IN HOME'
    PETS = 'PETS'
    OTHER = 'OTHER'

class Database:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.conn = pg8000.connect(user="postgres", password=config['postgres_pw'])
        self.cursor = self.conn.cursor()

def initEnums():
    db = Database()
    db.cursor.execute("DROP TYPE IF EXISTS role_type")
    db.cursor.execute("DROP TYPE IF EXISTS status_type")
    db.cursor.execute("DROP TYPE IF EXISTS region_type")
    db.cursor.execute("DROP TYPE IF EXISTS request_category")
    db.cursor.execute("CREATE TYPE role_type AS ENUM ('COMM MEMBER', 'EM AUTH')")
    db.cursor.execute("CREATE TYPE status_type AS ENUM ('OPEN', 'IN PROGRESS', 'FULFILLED')")
    db.cursor.execute("CREATE TYPE region_type AS ENUM ('ALBANY_CORVALLIS_PHILOMATH', 'PORTLAND_METRO', 'EUGENE', 'SALEM', 'DESCHUTES COUNTY', 'WASCO HOOD RIVER COUNTY', 'POLK YAMHILL COUNTY', 'MEDFORD ASHLAND', 'KING COUNTY', 'SPOKANE', 'WALLOWA')")

    db.cursor.execute("CREATE TYPE request_category AS ENUM ('GROCERY', 'PROJECT', 'FUNDS', 'IN HOME', 'PETS', 'OTHER')")
    db.conn.commit()
    
def initDB():
    db = Database()
    db.cursor.execute("DROP TABLE IF EXISTS requests")
    db.cursor.execute("SET timezone = 'America/Los_Angeles'")
    db.cursor.execute("CREATE TABLE requests (rID SERIAL NOT NULL, name VARCHAR(64) NOT NULL, region region_type NOT NULL, role role_type NOT NULL, title VARCHAR(64), agency VARCHAR(128), jurisdiction VARCHAR(128), email VARCHAR(64), phone VARCHAR(32), request_type request_category NOT NULL, details TEXT NOT NULL, status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateStarted TIMESTAMPTZ NOT NULL, dateFulfilled TIMESTAMPTZ NOT NULL, volunteers TEXT NOT NULL, PRIMARY KEY (rID))")
    db.conn.commit()
    return db

def initTest():
    db = Database()
    db.cursor.execute("DROP TABLE IF EXISTS test")
    db.cursor.execute("SET timezone = 'America/Los_Angeles'")
    db.cursor.execute("CREATE TABLE test (rID SERIAL NOT NULL, name VARCHAR(64) NOT NULL, region region_type NOT NULL, role role_type NOT NULL, title VARCHAR(64), agency VARCHAR(128), jurisdiction VARCHAR(128), email VARCHAR(64), phone VARCHAR(32), request_type request_category NOT NULL, details TEXT NOT NULL, status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateStarted TIMESTAMPTZ, dateFulfilled TIMESTAMPTZ, volunteers TEXT, PRIMARY KEY (rID))")
    db.conn.commit()
    return db

def test():
    db = Database() 
    
    name = 'test'
    region = Region.EUGENE
    role = Role.COMM
    email = 'test@test.com'
    phone = '(503) 123-4567'
    request_type = RequestType.OTHER
    detailsJSON = {'description': 'Test', 'additional_info': ''}
    details = json.dumps(detailsJSON)
    status = Status.OPEN
    dateOpened = datetime.now()
    
    db.cursor.execute("INSERT INTO test (name, region, role, email, phone, request_type, details, status, dateOpened) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING rID", (name, region, role, email, phone, request_type, details, status, dateOpened))
    db.conn.commit()
        
    results = db.cursor.fetchall()
    for row in results:
        print("New request ID: %s" % (row))
        rID = row.pop()

    db.cursor.execute("UPDATE test SET status = %s, dateFulfilled = %s WHERE rID = %s", (Status.FULFILLED, datetime.now(), rID))
    db.conn.commit()

    db.cursor.execute("SELECT * from test")
    db.conn.commit()

    results = db.cursor.fetchall()
    for row in results:
        print(row)

