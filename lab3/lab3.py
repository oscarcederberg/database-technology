from bottle import get, post, run, request, response
import sqlite3

PORT = 7007
RESET_SCRIPT = """
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;

CREATE TABLE users (
    username     TEXT NOT NULL,
    fullName    TEXT NOT NULL,
    pwd         TEXT NOT NULL,
    PRIMARY KEY  (username)
);

CREATE TABLE theaters (
    theater     TEXT NOT NULL,
    capacity    INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY  (theater)
);

CREATE TABLE movies (
    imdbKey     CHAR(9),
    title       TEXT NOT NULL,
    year        INTEGER NOT NULL,
    PRIMARY KEY (imdbKey)
);

CREATE TABLE performances (
    performanceId   TEXT DEFAULT (lower(hex(randomblob(16)))),
    theater         TEXT NOT NULL,
    imdbKey         CHAR(9),
    date            DATE,
    startTime       TIME,
    PRIMARY KEY (performanceId),
    FOREIGN KEY (theater) REFERENCES theaters(theater),
    FOREIGN KEY (imdbKey) REFERENCES movies(imdbKey)
);

CREATE TABLE tickets (
    ticketId        TEXT DEFAULT (lower(hex(randomblob(16)))),
    username        TEXT NOT NULL,
    performanceId   TEXT NOT NULL,
    PRIMARY KEY (ticketId),
    FOREIGN KEY (username) REFERENCES users(username),
    FOREIGN KEY (performanceId) REFERENCES performances(performanceId)
);

INSERT OR REPLACE
INTO theaters(theater, capacity)
VALUES ('Kino', 10),
('Regal', 16),
('Skandia', 100);
"""

db = sqlite3.connect("lab3.sqlite")

# sqlite3 lab3.sqlite < lab3-schema.sql
# We need to URLencode spaces and such before sending back strings
#

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

# get 	ping			            "pong" 200
@get('/ping')
def get_ping():
    response.status = 200
    return "pong"

# post	reset			            resets database
@post('/reset')
def post_reset():
    c = db.cursor()
    c.executescript(reset_script)
    return "Database reset"

# post	users			            ".../username" 201 / "" 400
@post('/users')
def post_users():
    user = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO        users(username, fullName, pwd)
        VALUES      ('?', '?', '?')
        RETURNING   last_insert_rowid()
        """,
        [user['username'], user['fullName'], user['pwd']]
    )
    found = c.fetchone()
    if not found:
        response.status = 400
        return ""
    else:
        db.commit()
        response.status = 201
        username, = found
        return f"http://localhost:{PORT}/users/{username}"

# post	movies			            ".../imdbkey" 201 / "" 400
@post('/movies')
def post_movies():
    movie = request.json
    c =sor()
    c.execute(
        """
        INSERT
        INTO        movies(imdbKey, title, year)
        VALUES      (?, ?, ?)
        RETURNING imdbKey
        """,
        [movie['imdbKey'], movie['title'], movie['year']]
    )
    found = c.fetchone()
    if not found:
        response.status = 400
        return ""
    else:
        db.commit()
        response.status = 201
        imdbKey, = found
        return f"http://localhost:{PORT}/movies/{imdbKey}"

# get	movies                      list with all movies
@get('/movies')
def get_movies():
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

# get	movies ?params              list with movies with params
@get('/movies')
def get_movies():
    query = """
        """
    params = []
    if request.query.title:
        query += ""
        params.append(unquote(request.query.title))
    c = db.cursor()
    c.execute(query, params)
    found = [{}]
    response.status = 200
    return {"data": found}

# get	movies/<key>                list with the movie or empty list
@get('/movies/<imdbKey>')
def get_movies(imdbKey):
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

# post	performances		        ".../perfid" 201 / "No such movie or theater" 400
@post('/performances')
def post_performances():
    performance = request.json
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    if not found:
        response.status = 400
        return "Illegal..."
    else:
        db.commit()
        response.status = 201
        _ = found
        return f""

# get	performances                list with all performances
@get('/performances')
def get_performances():
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

# post	tickets                     ".../<tickets_id>" 201 / "No tickets left" 400 / "Wrong user credentials" 401 / "Error" 400
@post('/tickets')
def post_tickets():
    ticket = request.json
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    if not found:
        response.status = 400
        return "Illegal..."
    else:
        db.commit()
        response.status = 201
        _ = found
        return f""

# get	users/<username>/tickets    list with all tickets of the user
@get('/users/<username>/tickets')
def get_tickets(username):
    c = db.cursor()
    c.execute(
        """
        """
    )
    found = [{}]
    response.status = 200
    return {"data": found}

run(host='localhost', port=PORT)