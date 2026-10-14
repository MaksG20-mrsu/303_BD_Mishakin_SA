#!/bin/bash
chcp 65001

sqlite3 movies_rating.db < db_init.sql

echo "1. Составить список фильмов, имеющих хотя бы одну оценку. Список фильмов отсортировать по году выпуска и по названиям. В списке оставить первые 10 фильмов."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT m.id, m.title, m.year FROM movies m WHERE EXISTS (SELECT 1 FROM ratings r WHERE r.movie_id = m.id) ORDER BY m.year, m.title LIMIT 10;"
echo " "

echo "2. Вывести список всех пользователей, фамилии (не имена!) которых начинаются на букву 'A'. Полученный список отсортировать по дате регистрации. В списке оставить первых 5 пользователей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT id, name, email, gender, register_date, occupation FROM users WHERE name LIKE '% A%' ORDER BY register_date LIMIT 5;"
echo " "

echo "3. Написать запрос, возвращающий информацию о рейтингах в более читаемом формате: имя эксперта, название фильма и год его выхода, оценка и дата оценки в формате ГГГГ-ММ-ДД. Отсортировать данные по имени эксперта, затем названию фильма и оценке. В списке оставить первые 50 записей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT u.name AS expert, m.title, m.year, r.rating, date(r.timestamp, 'unixepoch') AS rating_date FROM ratings r JOIN users u ON u.id = r.user_id JOIN movies m ON m.id = r.movie_id ORDER BY u.name, m.title, r.rating LIMIT 50;"
echo " "

echo "4. Вывести список фильмов с указанием тегов, которые были им присвоены пользователями. Приоритеты сортировки - год выпуска, затем название фильма, затем тег. В списке оставить первые 40 записей."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT m.title, m.year, t.tag FROM tags t JOIN movies m ON m.id = t.movie_id ORDER BY m.year, m.title, t.tag LIMIT 40;"
echo " "

echo "5. Вывести список самых свежих фильмов. В список должны войти все фильмы последнего года выпуска, имеющиеся в базе данных. Запрос должен быть универсальным, не зависящим от исходных данных (нужный год выпуска должен определяться в запросе, а не жестко задаваться)."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT id, title, year, genres FROM movies WHERE year = (SELECT MAX(year) FROM movies) ORDER BY title;"
echo " "

echo "6. Найти все комедии, выпущенные после 2000 года, которые понравились мужчинам (оценка не ниже 4.5). Для каждого фильма в этом списке вывести название, год выпуска и количество таких оценок. Результат отсортировать по году выпуска и названию фильма."
echo --------------------------------------------------
sqlite3 movies_rating.db -box -echo "SELECT m.title, m.year, COUNT(*) AS ratings_count FROM movies m JOIN ratings r ON r.movie_id = m.id JOIN users u ON u.id = r.user_id WHERE m.genres LIKE '%Comedy%' AND m.year > 2000 AND u.gender = 'male' AND r.rating >= 4.5 GROUP BY m.id, m.title, m.year ORDER BY m.year, m.title;"
echo " "

echo "7. Провести анализ занятий (профессий) пользователей - вывести количество пользователей для каждого рода занятий. Найти самую распространенную и самую редкую профессию посетитетей сайта."
echo --------------------------------------------------
echo "7.1. Количество пользователей по занятиям:"
sqlite3 movies_rating.db -box -echo "SELECT occupation, COUNT(*) AS users_count FROM users GROUP BY occupation ORDER BY users_count DESC, occupation;"
echo " "
echo "7.2. Самая распространенная профессия:"
sqlite3 movies_rating.db -box -echo "SELECT occupation, COUNT(*) AS users_count FROM users GROUP BY occupation HAVING COUNT(*) = (SELECT MAX(cnt) FROM (SELECT COUNT(*) AS cnt FROM users GROUP BY occupation)) ORDER BY occupation;"
echo " "
echo "7.3. Самая редкая профессия (если несколько с одинаковым количеством - выводятся все):"
sqlite3 movies_rating.db -box -echo "SELECT occupation, COUNT(*) AS users_count FROM users GROUP BY occupation HAVING COUNT(*) = (SELECT MIN(cnt) FROM (SELECT COUNT(*) AS cnt FROM users GROUP BY occupation)) ORDER BY occupation;"
echo " "