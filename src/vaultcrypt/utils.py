import random
from rich.console import Console

console = Console()

def show_quote(q: str):
    console.print("\n[bold cyan]💡 Today's reminder:[/bold cyan]")
    console.print(f"[italic]{q}[/italic]\n")
