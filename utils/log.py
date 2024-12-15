import logging
from rich import inspect
from rich.console import Console
from rich.logging import RichHandler

# Shared console
log_level = logging.DEBUG
console = Console()

#   Setup logger
FORMAT = "%(message)s"
logging.basicConfig(
    level=log_level, 
    format=FORMAT, 
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)
 
log = logging.getLogger("rich")