import typer
import os
import os.path as osp
from rich import print as rprint
from rich.table import Table
from rich.console import Console
from rich.markdown import Markdown
from book_epub import BookEPUB
from model import Model
import prompts
import warnings
warnings.filterwarnings('ignore')

BOOK_DIR = 'books/'
OUT_DIR = 'notes/books/'

app = typer.Typer(no_args_is_help=True)
console = Console()


def get_book_path_from_name(name: str) -> str:
    return osp.join(BOOK_DIR, name + ".epub")

def save_summary(content:str, name:str, title: str):
    save_dir = osp.join(OUT_DIR, name)
    ch_dir = osp.join(save_dir, title + ".md")
    os.makedirs(save_dir, exist_ok=True)        
    with open(ch_dir, 'w') as f:
        f.write(content)
    return ch_dir

def print_info(content: str):
   rprint("[bold yellow]INFO:[/bold yellow] {}".format(content))

@app.command()
def list_chapters(name: str):
    """
    List all chapters to pick for summarization
    from the book at the given book `name`.
    """
    book_path = get_book_path_from_name(name) 
    book_obj = BookEPUB(book_path)
    toc = book_obj.get_toc()
    table = Table("Index", "Chapter")
    for row in toc:
        table.add_row(*row)
    console.print(table)

# TODO: 1) Support range, and output to markdown file, 2) Model choice
@app.command()
def summarize(name: str, start_chapter: int = 1, model_type: str = "mistral", save: bool = False):
    model = Model(model_type)
    book_path = get_book_path_from_name(name)
    book_obj = BookEPUB(book_path)
    title = book_obj.get_chapter_title_from_index(start_chapter)
    print_info(
        "generating summary of chapter '{}' using model [green]{}[/green] :fire:"
        .format(title, model.qualified_name)
        )
    content = book_obj.get_content(start_chapter)
    resp = model.query(content, prompts.BOOK_SUMMARY_PROMPT)
    console.print(Markdown(resp["generated_text"].strip()))
    if save:
        out_dir = save_summary(resp['generated_text'].strip(), name, title)
        print_info("saved summary in [green]{}[/green].".format(out_dir))


if __name__ == "__main__":
    app()