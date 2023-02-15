from urllib.parse import unquote
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
    c.executescript(RESET_SCRIPT)
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
        VALUES      (?, ?, ?)
        RETURNING   username
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
        return f"/users/{username}"

# post	movies			            ".../imdbkey" 201 / "" 400
@post('/movies')
def post_movies():
    movie = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO        movies(imdbKey, title, year)
        VALUES      (?, ?, ?)
        RETURNING   imdbKey
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
        return f"/movies/{imdbKey}"

# get	movies                      list with all movies
# get	movies ?params              list with movies with params
@get('/movies')
def get_movies():
    query = """
        SELECT imdbKey, title, year
        FROM movies
        WHERE 1 = 1
        """
    params = []
    if request.query.title:
        query += " AND title == ?"
        params.append(unquote(request.query.title))
    if request.query.year:
        query += " AND year == ?"
        params.append(unquote(request.query.year))
    c = db.cursor()
    c.execute(query, params)
    found = [{"imdbKey":imdbKey, "title":title, "year":year} for imdbKey, title, year in c]
    response.status = 200
    return {"data": found}

# get	movies/<key>                list with the movie or empty list
@get('/movies/<imdbKey>')
def get_movies(imdbKey):
    c = db.cursor()
    c.execute(
        """
        SELECT imdbKey, title, year
        FROM movies
        WHERE imdbKey = ?
        """,
        [imdbKey]
    )
    found = [{"imdbKey": imdbKey, "title": title, "year": year}
        for imdbKey, title, year in c]
    response.status = 200
    return {"data": found}

# post	performances		        ".../perfid" 201 / "No such movie or theater" 400
@post('/performances')
def post_performances():
    performance = request.json
    c = db.cursor()
    c.execute(
        """
        INSERT
        INTO        performances(theater, imdbKey, date, startTime)
        VALUES      (?, ?, ?, ?)
        RETURNING   performanceId
        """,
        [performance['theater'], performance['imdbKey'], performance['date'], performance['time']]
    )
    found = c.fetchone()
    if not found:
        response.status = 400
        return "No such movie or theater"
    else:
        db.commit()
        response.status = 201
        performanceId, = found
        return f"/performances/{performanceId}"

# get	performances                list with all performances
@get('/performances')
def get_performances():
    c = db.cursor()
    c.execute(
        """
        WITH tickets_for_performance(performanceId, tickets) AS (
            SELECT performanceId, COUNT(*) as tickets
            FROM tickets
            GROUP BY performanceId
        )
        SELECT performanceId, date, startTime, movies.title, movies.year, theater, capacity - count(tickets) AS remainingSeats
        FROM performances
        LEFT OUTER JOIN movies USING (imdbKey)
        LEFT OUTER JOIN theaters USING (theater)
        LEFT OUTER JOIN tickets_for_performance USING (performanceId)
        """
    )
    found = [{"performanceId":performanceId, "date": date, "startTime":startTime, "title": title, "year":year, "theater":theater,"remainingSeats":remainingSeats}
                for performanceId, date, startTime, title, year, theater, remainingSeats in c]
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
        WITH tickets_for_user(username, performanceId, tickets) AS (
            SELECT performanceId, username, COUNT(*) as tickets
            FROM tickets
            GROUP BY performanceId, username
        )
        SELECT date, startTime, theater, title, year, count(tickets) as nbrOfTickets
        FROM tickets
        JOIN performances ON (performanceId)
        JOIN tickets_for_user ON (username)
        WHERE username = ?
        """,
        [username]
    )
    found = [{"date": date, "startTime": startTime, "theater": theater, "title": title, "year": year, "nbrOfTickets": nbrOfTickets}
        for date, startTime, theater, title, year, nbrOfTickets in c]
    response.status = 200
    return {"data": found}

run(host='localhost', port=PORT)