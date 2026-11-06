CREATE TABLE IF NOT EXISTS GENRES (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        url TEXT UNIQUE,
        img TEXT,
        favorite BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS MUSIC (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        id_autor INTEGER NOT NULL,
        id_genre INTEGER NOT NULL,
        file TEXT NOT NULL,
        img TEXT,
        _time TEXT,
        FOREIGN KEY (id_autor) REFERENCES AUTOR (id),
        FOREIGN KEY (id_genre) REFERENCES GENRES (id),
        UNIQUE(name)
);

CREATE TABLE IF NOT EXISTS AUTOR (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        UNIQUE(name)
)