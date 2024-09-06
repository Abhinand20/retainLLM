from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from your Next.js app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOK_DIR = "books/"


def get_book_names():
    idx = 1
    id_to_name = {}
    for book_path in os.listdir(BOOK_DIR):
        if book_path.endswith(".epub"):
            id_to_name[idx] = book_path.split(".epub")[0]
            idx += 1
    return id_to_name

@app.get("/book/list")
def list_books():
    books = []
    id_to_name = get_book_names()
    for k,v in id_to_name.items():
        books.append({"id":k, "name":v})
    return books