USE url_database;

CREATE TABLE url_hits (
    short_url VARCHAR(50) PRIMARY KEY,
    long_url TEXT NOT NULL,
    hit INT DEFAULT 0
);

INSERT INTO url_hits (short_url, long_url, hit) VALUES
    ('y8HOfS', 'https://youtu.be/XHjmvilKanM?si=kpQuCbTzgPo2yH7t', 13),
    ('lens-studio', 'https://lu.ma/aohptfvf', 283),
    ('jmi-ar', 'https://lu.ma/aohptfvf', 102),
    ('dZzz5r', 'https://youtu.be/_rTOnl251Yg', 11),
    ('piet-ar', 'https://lu.ma/aohptfvf', 15),
    ('meta-spark', 'https://lu.ma/6yidyvlu', 51);
