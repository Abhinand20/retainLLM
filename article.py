
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
import pdfparser
warnings.filterwarnings('ignore')

PDF_DIR = 'articles/'
OUT_DIR = 'notes/articles/'

app = typer.Typer(no_args_is_help=True)
console = Console()


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
def list_sections(pdf_path: str):
    """
    List all sections to pick for summarization
    from the pdf article.
    """
    fulltext = pdfparser.parse_pdf_to_dict(pdf_path)
    table = Table("Index", "Section")
    for idx, sec in enumerate(fulltext['sections']):
        table.add_row(str(idx), sec['heading'])
    console.print(table)


if __name__ == "__main__":
    app()