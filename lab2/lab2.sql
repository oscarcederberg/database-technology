PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS theatres;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS performances;
DROP TABLE IF EXISTS tickets;

PRAGMA foreign_keys=ON;

CREATE TABLE customers (
    username     TEXT NOT NULL,
    name         TEXT NOT NULL,
    password     TEXT NOT NULL,
    PRIMARY KEY  (username)
);

CREATE TABLE theatres (
    name         TEXT NOT NULL,
    capacity     INTEGER NOT NULL CHECK (capacity > 0),
    PRIMARY KEY  (name)
);

CREATE TABLE movies (
    imdb_id     CHAR(9),
    title       TEXT NOT NULL,
    year        INTEGER NOT NULL,
    time        INTEGER NOT NULL CHECK (time > 0),
    PRIMARY KEY (imdb_id)
);

CREATE TABLE performances (
    performance_id  TEXT DEFAULT (lower(hex(randomblob(16)))),
    name            TEXT NOT NULL,
    imdb_id         CHAR(9),
    date            DATE,
    time            TIME,
    PRIMARY KEY (performance_id),
    FOREIGN KEY (name) REFERENCES theatres(name),
    FOREIGN KEY (imdb_id) REFERENCES movies(imdb_id)
);

CREATE TABLE tickets (
    ticket_id       TEXT DEFAULT (lower(hex(randomblob(16)))),
    username        TEXT NOT NULL,
    performance_id  TEXT NOT NULL,
    PRIMARY KEY (ticket_id),
    FOREIGN KEY (username) REFERENCES customers(username),
    FOREIGN KEY (performance_id) REFERENCES performances(performance_id)
);

INSERT OR REPLACE
INTO customers(username, name, password)
VALUES ('abc', 'Göran Persson', 'lösenord1'),
('def', "Klas Petter", "lösenord2"),
('ghi', "Tove Styrke", "lösenord3");

INSERT OR REPLACE
INTO theatres(name, capacity)
VALUES ('Filmstaden Lund', 200),
('Filmstaden Malmö', 400),
('Filmstaden Eslöv', 2);

INSERT OR REPLACE
INTO movies(imdb_id, title, year, time)
VALUES ('dc1234567', 'Dösjebro Calling', 2010, 180),
('ts0000000', 'Trainspotting', 1980, 167),
('nn1234567', "Någon film", 2000, 80);

INSERT OR REPLACE
INTO performances(performance_id, name, imdb_id, date, time)
VALUES (lower(hex(randomblob(16))), 'Filmstaden Lund', 'dc1234567', '2022-02-08', '18:30'),
( lower(hex(randomblob(16))) , 'Filmstaden Lund', 'dc1234567', '2022-02-08', '22:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Lund', 'dc1234567', '2022-02-09', '18:30'),
( lower(hex(randomblob(16))) , 'Filmstaden Lund', 'ts0000000', '2022-02-08', '22:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Malmö', 'dc1234567', '2022-02-08', '16:30'),
( lower(hex(randomblob(16))) , 'Filmstaden Malmö', 'nn1234567', '2022-02-08', '20:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Eslöv', 'nn1234567', '2022-02-08', '12:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Eslöv', 'nn1234567', '2022-02-08', '14:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Eslöv', 'nn1234567', '2022-02-08', '16:00'),
( lower(hex(randomblob(16))) , 'Filmstaden Eslöv', 'nn1234567', '2022-02-08', '18:00');