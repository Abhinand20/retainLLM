from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from book_epub import BookEPUB
import os.path as osp


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOK_DIR = "books/"
BOOK_ID_MAP = dict()

def get_book_names():
    idx = 1
    id_to_name = {}
    for book_path in os.listdir(BOOK_DIR):
        if book_path.endswith(".epub"):
            id_to_name[idx] = book_path.split(".epub")[0]
            idx += 1
    return id_to_name

def get_book_path_from_name(name: str) -> str:
    return osp.join(BOOK_DIR, name + ".epub")


BOOK_ID_MAP = get_book_names()

@app.get("/book/list")
def list_books():
    books = []
    for k,v in BOOK_ID_MAP.items():
        books.append({"id":k, "name":v})
    return books


@app.get("/book/chapter/list")
def list_chapters(book_id: int = 1):
    if book_id not in BOOK_ID_MAP:
        raise HTTPException(404, detail="Could not find the requested book.")
    chapters = []
    book_name = BOOK_ID_MAP[book_id]
    book_path = get_book_path_from_name(book_name) 
    book_obj = BookEPUB(book_path)
    toc = book_obj.get_toc()
    for idx,title in toc:
        chapters.append({"id":idx, "title":title})
    return chapters