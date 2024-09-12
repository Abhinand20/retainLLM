from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from youtube_transcript_api import YouTubeTranscriptApi
import os
from model import model_factory
from book_epub import BookEPUB
import os.path as osp
import prompts
from podcast import process_transcript, extract_video_id


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


@app.get("/book/summary/v1")
def summarize_chapter(book_id: int, chapter_ids: str, model_type: str = "gemini"):
    if book_id not in BOOK_ID_MAP:
        raise HTTPException(404, detail="Could not find the requested book.")
    ch_ids = chapter_ids.split(",")
    book_name = BOOK_ID_MAP[book_id] 
    start_chapter = int(ch_ids[0])
    model = model_factory(model_type, prompts.BOOK_SUMMARY_PROMPT)
    book_path = get_book_path_from_name(book_name)
    book_obj = BookEPUB(book_path)
    title = book_obj.get_chapter_title_from_index(start_chapter)
    content = book_obj.get_content(start_chapter)
    resp = model.query(content) 
    return {"summary":resp}

@app.get("/podcast/summary/v1")
def summarize_podcast(yt_video_link: str, model_type: str = "gemini"):
    video_id = extract_video_id(yt_video_link)
    model = model_factory(model_type, prompts.PODCAST_SUMMARY_PROMPT)
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise HTTPException(404, detail="Could not fetch YT transcript.")
    content = process_transcript(transcript)
    resp = model.query(content) 
    return {"summary":resp}