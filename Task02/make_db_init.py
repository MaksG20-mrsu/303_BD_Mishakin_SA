import os
import csv
import sqlite3
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_FILE = os.path.join(BASE_DIR, "db_init.sql")

def num(value):
    return "NULL" if value is None or value == "" else str(value)

def path(name):
    return os.path.join(BASE_DIR, name)

def q(value):
    if value is None or value == "":
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"

def escape_sql(value):

    if value is None:
        return 'NULL'
    return str(value).replace("'", "''")

def main():
    lines = []
    w = lines.append
    w("PRAGMA foreign_keys = OFF;")
    w("DROP TABLE IF EXISTS movies;")
    w("DROP TABLE IF EXISTS ratings;")
    w("DROP TABLE IF EXISTS tags;")
    w("DROP TABLE IF EXISTS users;")
    w("")
    w("CREATE TABLE movies (")
    w("    id INTEGER PRIMARY KEY,")
    w("    title VARCHAR(160) NOT NULL,")
    w("    year INTEGER,")
    w("    genres VARCHAR(80)")
    w(");")
    w("CREATE TABLE ratings (")
    w("    id INTEGER PRIMARY KEY AUTOINCREMENT,")
    w("    user_id INTEGER NOT NULL,")
    w("    movie_id INTEGER NOT NULL,")
    w("    rating REAL NOT NULL,")
    w("    timestamp INTEGER NOT NULL")
    w(");")
    w("CREATE TABLE tags (")
    w("    id INTEGER PRIMARY KEY AUTOINCREMENT,")
    w("    user_id INTEGER NOT NULL,")
    w("    movie_id INTEGER NOT NULL,")
    w("    tag VARCHAR(100) NOT NULL,")
    w("    timestamp INTEGER NOT NULL")
    w(");")
    w("CREATE TABLE users (")
    w("    id INTEGER PRIMARY KEY,")
    w("    name VARCHAR(50) NOT NULL,")
    w("    email VARCHAR(50),")
    w("    gender VARCHAR(10),")
    w("    register_date TEXT,")
    w("    occupation VARCHAR(20)")
    w(");")
    w("")
    w("BEGIN TRANSACTION;")

    with open(path("movies.csv"), encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)  # заголовок
        for row in reader:
            if not row:
                continue
            movie_id, title, genres = row[0], row[1].strip(), row[2]
            m = re.search(r"\((\d{4})\)\s*$", title)
            year = m.group(1) if m else None
            if m:
                title = title[:m.start()].strip()
            w("INSERT INTO movies (id, title, year, genres) VALUES (%s, %s, %s, %s);"
              % (movie_id, q(title), num(year), q(genres)))


    with open(path("ratings.csv"), encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row:
                continue
            w("INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES (%s, %s, %s, %s);"
              % (row[0], row[1], row[2], row[3]))


    with open(path("tags.csv"), encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if not row:
                continue
            w("INSERT INTO tags (user_id, movie_id, tag, timestamp) VALUES (%s, %s, %s, %s);"
              % (row[0], row[1], q(row[2]), row[3]))


    with open(path("users.txt"), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = line.split("|")
            w("INSERT INTO users (id, name, email, gender, register_date, occupation) "
              "VALUES (%s, %s, %s, %s, %s, %s);"
              % (p[0], q(p[1]), q(p[2]), q(p[3]), q(p[4]), q(p[5])))

    w("COMMIT;")

    with open(OUT_FILE, "w", encoding="utf-8", newline="\n") as out:
        out.write("\n".join(lines) + "\n")
    print("Файл успешно создан.")


if __name__ == "__main__":
    main()
