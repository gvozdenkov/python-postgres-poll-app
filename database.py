import datetime
from typing import List, Tuple
import psycopg2
from psycopg2.extras import execute_values
from config import config

def connectPostgre():
    conn = None
    try:
        params = config(filename = 'database.ini', section = 'postgresql')
        print(f"Connecting to the PostgreSQL database '{params['database']}'...\n")
        # print(params)
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



connection = connectPostgre()

Poll = Tuple[int, str, str]
Vote = Tuple[str, int]
PollwithOption = Tuple[int, str, str, int, str, int]
PollResults = Tuple[str, int, str, int, float]

CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls (
    id SERIAL PRIMARY KEY,
    title TEXT,
    owner TEXT,
    relaeas_timestamp REAL
);"""

CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options (
    option_id SERIAL PRIMARY KEY,
    option_text TEXT,
    poll_id INTEGER,
    FOREIGN KEY(poll_id) REFERENCES polls(id)
);"""

CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes (
    username TEXT,
    option_id INTEGER
);"""

INSERT_POLL = "INSERT INTO polls (title, owner, relaeas_timestamp) VALUES (%s, %s, %s) RETURNING id;"
INSERT_OPTION = "INSERT INTO options (poll_id, option_text) VALUES %s;"
INSERT_VOTE = "INSERT INTO votes (option_id, username) VALUES (%s, %s);"
SELECT_ALL_POLLS = "SELECT * FROM polls;"

SELECT_POLL_WITH_OPTIONS = """
    SELECT * FROM polls
    JOIN options ON polls.id = options.poll_id
    WHERE polls.id = %s
;"""

SELECT_POLL = "SELECT * FROM polls WHERE polls.id = %s;"

SELECT_LATEST_POLL = """
    WITH latest_id AS (
        SELECT id FROM polls ORDER BY id DESC LIMIT 1
    )

    SELECTN * FROM polls
    JOIN options ON polls.id = options.option_id
    WHERE polls.id = latest_id

;"""

SELECT_RANDOME_VOTE = "SELECT * FROM votes WHERE option_id = %s ORDER BY RANDOM() LIMIT 1;"

SELECT_VOTE_RESULTS = """
    SELECT
        polls.title,
        options.option_id,
        options.option_text,
        count(votes.option_id) as vote_count,
        count(votes.option_id) / sum(count(votes.option_id)) over() * 100 as vote_persant
    FROM options
    JOIN votes on votes.option_id = options.option_id
    JOIN polls on polls.id = options.poll_id
    WHERE options.poll_id = %s
    GROUP BY options.option_id, polls.title;


;"""

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_POLLS)
            cursor.execute(CREATE_OPTIONS)
            cursor.execute(CREATE_VOTES)

def create_poll(title: str, owner: str, options: List[str]):
    with connection:
        with connection.cursor() as cursor:
            ts = datetime.datetime.now().timestamp()
            cursor.execute(INSERT_POLL, (title, owner, ts,))
            poll_id = cursor.fetchone()[0]

            option_values = [(poll_id, option_text) for option_text in options]
            execute_values(cursor, INSERT_OPTION, option_values)

def add_option(poll_id: int, option_text: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_OPTION, (poll_id, option_text,))

def add_vote(option_id: str, username: str):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_VOTE, (option_id, username,))

def get_all_polls() -> list[Poll]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_POLLS)
            return cursor.fetchall()

def get_poll(id: int) -> Poll:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL, (id,))
            return cursor.fetchone()

def get_poll_options(poll_id: int) -> list[PollwithOption]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_POLL_WITH_OPTIONS, (poll_id,))
            return cursor.fetchall()

def get_poll_and_vote_results(poll_id: int) -> list[PollResults]:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_VOTE_RESULTS, (poll_id,))
            return cursor.fetchall()


def get_random_poll_vote(option_id: int) -> Vote:
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_RANDOME_VOTE, (option_id,))
            return cursor.fetchone()

