DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    username     TEXT NOT NULL,
    name         TEXT NOT NULL,
    password     TEXT NOT NULL,
    PRIMARY KEY  (username)
);

DROP TABLE IF EXISTS theatres;
CREATE TABLE theatres (
    name         TEXT NOT NULL,
    capacity     INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY  (name)
);

DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
    imdb_id     CHAR(9),
    title       TEXT NOT NULL,
    year        INTEGER NOT NULL,
    time        INTEGER NOT NULL CHECK (time > 0),
    PRIMARY KEY (imdb_id)
);

DROP TABLE IF EXISTS performances;
CREATE TABLE performances (
    performance_id  TEXT DEFAULT (lower(hex(randomblob(16)))),
    name            TEXT NOT NULL,
    imdb_id         CHAR(9),
    starttime       DATETIME,
    PRIMARY KEY (performance_id),
    FOREIGN KEY (name) REFERENCES theatres.name,
    FOREIGN KEY (imdb_id) REFERENCES movies.imdb_id
);

DROP TABLE IF EXISTS tickets;
CREATE TABLE tickets (
    ticket_id       TEXT DEFAULT (lower(hex(randomblob(16)))),
    username        TEXT NOT NULL,
    performance_id  TEXT NOT NULL,
    PRIMARY KEY (ticket_id),
    FOREIGN KEY (username) REFERENCES customers.username,
    FOREIGN KEY (performance_id) REFERENCES performances.performance_id
)