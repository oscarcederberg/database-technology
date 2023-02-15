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