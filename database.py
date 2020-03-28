import pg8000
import json

class Database:
    def __init__(self):
        with open('config.json') as f:
            config = json.load(f)
        self.conn = pg8000.connect(user="postgres", password=config['postgres_pw'])
        self.cursor = conn.cursor()

def initDB():
    db = Database()
    db.cursor.execute("DROP TABLE IF EXISTS requests")
    db.cursor.execute("CREATE TYPE role_type AS ENUM ('COMM MEMBER', 'EM AUTH')")
    db.cursor.execute("CREATE TYPE status_type AS ENUM ('OPEN', 'FULFILLED')")
    db.cursor.execute("SET timezone = 'America/Los_Angeles'")
    db.cursor.execute("CREATE TABLE requests (rID INT NOT NULL, name VARCHAR(64) NOT NULL, role role_type NOT NULL, email VARCHAR(64), phone VARCHAR(32), request VARCHAR(600), status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateFulfilled TIMESTAMPTZ NOT NULL, PRIMARY KEY (rID))")
    db.conn.commit()
    return db
