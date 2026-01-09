from fastapi import FastAPI
from palindrome import is_palindrome

app=FastAPI()
@app.get("/")
def home():
    return {"Note": "FastAPI in running"}

@app.get("/palindrome/{str1}")
def palindrome(str1: str):
    return {
        "str1": str1,
        "is_palindrome": is_palindrome(str1)
    }
