PRAGMA foreign_keys = ON;

INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES ('Богдан', 'Малухин', 'mbe@yandex.com', 'male', date('now'),
        (SELECT id FROM occupations WHERE name = 'student'));
INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES ('Илья', 'Марусин', 'mid@yandex.com', 'male', date('now'),
        (SELECT id FROM occupations WHERE name = 'student'));
INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES ('Даниил', 'Меньшаков', 'mln@yandex.com', 'male', date('now'),
        (SELECT id FROM occupations WHERE name = 'student'));
INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES ('Михаил', 'Мехонцев', 'mmv@yandex.com', 'male', date('now'),
        (SELECT id FROM occupations WHERE name = 'student'));
INSERT INTO users (first_name, last_name, email, gender, register_date, occupation_id)
VALUES ('Сергей', '︎Мишакин', 'msa@yandex.com', 'male', date('now'),
        (SELECT id FROM occupations WHERE name = 'student'));

INSERT INTO movies (title, year) VALUES ('Morbius', 2022);
INSERT INTO movies (title, year) VALUES ('Cargo 200', 2007);
INSERT INTO movies (title, year) VALUES ('LoTR: The Gang and the Ring - Localized by Goblin', 2001);

INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id FROM movies m, genres g
WHERE m.title = 'Morbius' AND m.year = 2022 AND g.name = 'Action';
INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id FROM movies m, genres g
WHERE m.title = 'Cargo 200' AND m.year = 2007 AND g.name = 'Thriller';
INSERT INTO movie_genres (movie_id, genre_id)
SELECT m.id, g.id FROM movies m, genres g
WHERE m.title = 'LoTR: The Gang and the Ring - Localized by Goblin' AND m.year = 2001 AND g.name IN ('Adventure', 'Comedy', 'Fantasy');


INSERT INTO ratings (user_id, movie_id, rating, timestamp)
VALUES ((SELECT id FROM users WHERE email = 'msa@yandex.com'),
        (SELECT id FROM movies WHERE title = 'Morbius' AND year = 2022),
        5.0, CAST(strftime('%s', 'now') AS INTEGER));
INSERT INTO ratings (user_id, movie_id, rating, timestamp)
VALUES ((SELECT id FROM users WHERE email = 'msa@yandex.com'),
        (SELECT id FROM movies WHERE title = 'Cargo 200' AND year = 2007),
        5.0, CAST(strftime('%s', 'now') AS INTEGER));
INSERT INTO ratings (user_id, movie_id, rating, timestamp)
VALUES ((SELECT id FROM users WHERE email = 'msa@yandex.com'),
        (SELECT id FROM movies WHERE title = 'LoTR: The Gang and the Ring - Localized by Goblin' AND year = 2001),
        5.0, CAST(strftime('%s', 'now') AS INTEGER));