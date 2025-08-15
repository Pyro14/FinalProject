import sqlite3 as sql

db_path = "C:/Users/manuf/PycharmProjects/FinalProject/database/users.db"

query = f""" 
SELECT
    *
FROM
    movies s
LEFT JOIN
    fav_movies f
ON s.id = f.movies_id
WHERE
   f.user_id = 5"""
con = sql.connect(db_path)
cur = con.cursor()
cur.execute(query)
result = cur.fetchall()
con.close()

print(result)