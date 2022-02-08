import psycopg2
import os


def create_table():
    command = """create table wordle(
    username VARCHAR(50),
    score INT NOT NULL,
    played_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CHECK (score between 0 AND 6),
    constraint pk_wordle PRIMARY KEY (username, played_at));
    """

    conn = None
    try:
        DB_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        if conn is not None:
            print("done")
            conn.close()
