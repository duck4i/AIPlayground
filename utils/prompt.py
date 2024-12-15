import typer 
import click
from rich.prompt import Prompt
from utils import console

def promptIntRange(text: str, min: int, max: int):
    return typer.prompt(text, type=click.IntRange(min=min, max=max))

def promptText(text: str, default: str = None):
    return Prompt(console=console).ask(prompt=text, default=default)