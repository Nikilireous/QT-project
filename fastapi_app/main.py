from fastapi import FastAPI, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from bcrypt import hashpw, checkpw, gensalt
import sqlite3


app = FastAPI()
absolute_path = "fastapi_app/"


@app.get("/")
async def index():
    return {"works": True}


@app.get("/posters")
async def get_existing_posters():
    answer = {}
    sql_request = '''SELECT
                        Poster.CompositionId,
                        Poster.Title,
                        Genre.GenreName,
                        Poster.Time,
                        Theatres.TheatreName,
                        Poster.Price
                    FROM
                            Poster
                        LEFT JOIN Genre ON Poster.GenreId = Genre.GenreId
                        LEFT JOIN Theatres ON Poster.TheatreId = Theatres.TheatreId'''

    con = sqlite3.connect(f"{absolute_path}all_data/poster_data.db")
    cur = con.cursor()

    poster_table = cur.execute(sql_request).fetchall()
    con.close()

    for row in poster_table:
        answer[row[0]] = row[1:]

    return answer
