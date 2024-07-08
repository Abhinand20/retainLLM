"""
A CLI that takes in a book name (.epub for now) and optionally chapter.
Uses an LLM to generate bullet points for the most important takeaways
from a chapter(s).
"""
from pprint import pprint
from book_epub import BookEPUB
from model import Model
import warnings
warnings.filterwarnings('ignore')

BOOK_PATH = 'books/thinking_fast_and_slow.epub'

def main():    
    book_obj = BookEPUB(BOOK_PATH)
    # print(book_obj.getTitle())
    print(book_obj.getTOC())
    # content = book_obj.getContentInRange(10,12)
    # print(content)
    # model = Model('mistral')
    # resp = model.query(content)
    # print(resp["generated_text"].split("<|assistant|>")[-1])
    # print(resp)

if __name__ == '__main__':
    main()