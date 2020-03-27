import pg8000
import json

def initDB():
    with open('config.json') as f:
        config = json.load(f)
    conn = pg8000.connect(user="postgres", password=config['postgres_pw'])
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS requests")
    cursor.execute("CREATE TYPE role_type AS ENUM ('COMM MEMBER', 'EM AUTH')")
    cursor.execute("CREATE TYPE status_type AS ENUM ('OPEN', 'FULFILLED')")
    cursor.execute("SET timezone = 'America/Los_Angeles'")
    cursor.execute("CREATE TABLE requests (rID INT NOT NULL, name VARCHAR(64) NOT NULL, role role_type NOT NULL, email VARCHAR(64), phone VARCHAR(32), request VARCHAR(600), status status_type NOT NULL, dateOpened TIMESTAMPTZ NOT NULL, dateFulfilled TIMESTAMPTZ NOT NULL, PRIMARY KEY (rID))")
    conn.commit()
    return conn, cursor
