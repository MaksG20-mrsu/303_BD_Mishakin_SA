import os
import csv
import sqlite3

DB_NAME = 'movies_rating.db'
SQL_SCRIPT_NAME = 'db_init.sql'
DATA_DIR = 'dataset'

def escape_sql(value):
    """Экранирует одинарные кавычки для безопасной вставки в SQL."""
    if value is None:
        return 'NULL'
    return str(value).replace("'", "''")

def generate_sql_script():
    """Генерирует SQL-скрипт db_init.sql."""
    print(f"Генерация {SQL_SCRIPT_NAME}...")
    
    with open(SQL_SCRIPT_NAME, 'w', encoding='utf-8') as f:
        f.write("DROP TABLE IF EXISTS movies;\n")
        f.write("DROP TABLE IF EXISTS ratings;\n")
        f.write("DROP TABLE IF EXISTS tags;\n")
        f.write("DROP TABLE IF EXISTS users;\n\n")

        f.write("""CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    genres TEXT
);\n\n""")

        f.write("""CREATE TABLE ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL,
    timestamp INTEGER NOT NULL
);\n\n""")

        f.write("""CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    tag TEXT,
    timestamp INTEGER NOT NULL
);\n\n""")

        f.write("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    gender TEXT,
    register_date TEXT,
    occupation TEXT
);\n\n""")

        movies_path = os.path.join(DATA_DIR, 'movies.csv')
        if os.path.exists(movies_path):
            with open(movies_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    movie_id = row.get('movieId') or row.get('id')
                    title = row.get('title', '')
                    genres = row.get('genres', '')
                    year = 'NULL'
                    if '(' in title and ')' in title:
                        try:
                            year_str = title[title.rfind('(')+1:title.rfind(')')]
                            if year_str.isdigit():
                                year = year_str
                        except:
                            pass
                    f.write(f"INSERT INTO movies (id, title, year, genres) VALUES ({movie_id}, '{escape_sql(title)}', {year}, '{escape_sql(genres)}');\n")

        ratings_path = os.path.join(DATA_DIR, 'ratings.csv')
        if os.path.exists(ratings_path):
            with open(ratings_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user_id = row.get('userId')
                    movie_id = row.get('movieId')
                    rating = row.get('rating')
                    timestamp = row.get('timestamp')
                    f.write(f"INSERT INTO ratings (user_id, movie_id, rating, timestamp) VALUES ({user_id}, {movie_id}, {rating}, {timestamp});\n")

        tags_path = os.path.join(DATA_DIR, 'tags.csv')
        if os.path.exists(tags_path):
            with open(tags_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    user_id = row.get('userId')
                    movie_id = row.get('movieId')
                    tag = row.get('tag', '')
                    timestamp = row.get('timestamp')
                    f.write(f"INSERT INTO tags (user_id, movie_id, tag, timestamp) VALUES ({user_id}, {movie_id}, '{escape_sql(tag)}', {timestamp});\n")

        users_path = os.path.join(DATA_DIR, 'users.txt')
        if os.path.exists(users_path):
            with open(users_path, 'r', encoding='utf-8') as txtfile:
                for line in txtfile:
                    line = line.strip()
                    if not line: continue
                    parts = line.split('|')
                    if len(parts) >= 6:
                        user_id, name, email, gender, reg_date, occupation = parts[:6]
                        f.write(f"INSERT INTO users (id, name, email, gender, register_date, occupation) VALUES ({user_id}, '{escape_sql(name)}', '{escape_sql(email)}', '{escape_sql(gender)}', '{escape_sql(reg_date)}', '{escape_sql(occupation)}');\n")

    print(f"Скрипт {SQL_SCRIPT_NAME} успешно создан.")

def execute_sql_script():
    
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    with open(SQL_SCRIPT_NAME, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    try:
        cursor.executescript(sql_script)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при выполнении SQL-скрипта: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    generate_sql_script()
    execute_sql_script()
