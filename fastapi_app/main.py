from fastapi import FastAPI, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from bcrypt import hashpw, checkpw, gensalt


app = FastAPI()


@app.get("/")
def index():
    return {"works": True}
