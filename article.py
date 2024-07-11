
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


def print_info(content: str):
   rprint("[bold yellow]INFO:[/bold yellow] {}".format(content))

def print_error(content: str):
   rprint("[bold red]ERROR:[/bold red] {}".format(content))

def save_summary(out_dir: str, content: str, name: str, title: str):
    save_dir = osp.join(out_dir, name)
    ch_dir = osp.join(save_dir, title + ".md")
    os.makedirs(save_dir, exist_ok=True)        
    with open(ch_dir, 'w') as f:
        f.write(content)
    return ch_dir

def combine_pdf_content(sections, title, abstract = None):
    content = [title]
    if abstract:
        content.append(abstract)
    for section in sections:
        content.append(section['heading'] + '\n' + section['text'])    
    return "\n".join(content)

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

"""
TODO:
    1. Add a new prompt for discussing only the provided sections.
    2. Add support for parsing images/tables for the LLM input.
"""
@app.command()
def summarize(pdf_path: str, section_start: int = 0, section_end: int = -1, model_type: str = "mistral", save: bool = False):
    model = Model(model_type)
    pdf_name = pdf_path.split(osp.sep)[-1]
    fulltext = pdfparser.parse_pdf_to_dict(pdf_path)
    max_sections = len(fulltext['sections']) - 1
    if section_end == -1:
        section_end = max_sections 
    if section_end < section_start:
        print_error("section-end cannot be greater than section-start")
        return
    if section_end > max_sections or section_start > max_sections:
        print_error("section index cannot be greater than {}".format(max_sections))
        return
    title = fulltext['title']
    sections = fulltext['sections']
    include_abstract = section_start == 0 and section_end == max_sections
    print_info(
        "generating summary of paper titled '{}' using model [green]{}[/green] :fire:"
        .format(title, model.qualified_name)
        )
    print_info("CONTENT_RANGE: [{}, {}]".format(
        sections[section_start]['heading'],
        sections[section_end]['heading'],
        ))
    content = combine_pdf_content(
        sections[section_start:section_end + 1],
        title,
        fulltext['abstract'] if include_abstract else None
    )
    print(content)
    resp = model.query(content, prompts.PAPER_SUMMARY_PROMPT)
    console.print(Markdown(resp["generated_text"].strip()))
    if save:
        out_dir = save_summary(OUT_DIR, resp['generated_text'].strip(), pdf_name, title)
        print_info("saved summary in [green]{}[/green].".format(out_dir))

if __name__ == "__main__":
    app()