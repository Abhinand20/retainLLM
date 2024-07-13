
from rich import print as rprint

def print_info(content: str):
   rprint("[bold yellow]INFO:[/bold yellow] {}".format(content))

def print_error(content: str):
   rprint("[bold red]ERROR:[/bold red] {}".format(content))
