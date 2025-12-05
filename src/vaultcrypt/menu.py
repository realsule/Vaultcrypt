from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
import subprocess
import sys
import os

console = Console()

def run(cmd: str):
    """Run a python -m vaultcrypt.cli command internally."""
    full_cmd = f"{sys.executable} -m vaultcrypt.cli {cmd}"
    os.system(full_cmd)

def main_menu():
    while True:
        console.print(Panel("""
[bold cyan]VAULTCRYPT INTERACTIVE MENU[/bold cyan]

[green]1.[/green] Generate Password  
[green]2.[/green] Add Password Entry  
[green]3.[/green] List Entries  
[green]4.[/green] View Entry  
[green]5.[/green] Remove Entry  
[green]6.[/green] Encrypt File  
[green]7.[/green] Decrypt File  
[green]8.[/green] Bulk Encrypt Folder  
[green]9.[/green] Exit
        """, title="🔐 Vaultcrypt"))

        choice = IntPrompt.ask("[bold yellow]Choose an option[/bold yellow]")

        if choice == 1:
            length = IntPrompt.ask("Password length", default=16)
            run(f"generate-password --length {length} --symbols")

        elif choice == 2:
            title = Prompt.ask("Title (eg: Instagram)")
            username = Prompt.ask("Username/email")
            password = Prompt.ask("Password (leave empty to auto-generate)", default="")
            tag = Prompt.ask("Tag (eg: personal/work)")
            owner = Prompt.ask("Owner", default="local")

            cmd = f'add-entry --title "{title}" --username "{username}" --tag "{tag}" --owner "{owner}"'
            if password.strip():
                cmd += f' --password "{password}"'
            run(cmd)

        elif choice == 3:
            owner = Prompt.ask("Owner filter", default="local")
            run(f"list-entries --owner {owner}")

        elif choice == 4:
            entry_id = IntPrompt.ask("Entry ID to view")
            reveal = Prompt.ask("Reveal password? (y/n)", default="n")
            flag = "--reveal True" if reveal.lower() == "y" else ""
            run(f"get-entry {entry_id} {flag}")

        elif choice == 5:
            entry_id = IntPrompt.ask("Entry ID to delete")
            run(f"remove-entry {entry_id} --confirm")

        elif choice == 6:
            file_path = Prompt.ask("File to encrypt")
            key = Prompt.ask("Path to file key (eg: filekey.key)")
            run(f'encrypt-file "{file_path}" --key "{key}"')

        elif choice == 7:
            file_path = Prompt.ask("Encrypted file")
            key = Prompt.ask("Key path")
            run(f'decrypt-file "{file_path}" --key "{key}"')

        elif choice == 8:
            folder = Prompt.ask("Folder to encrypt")
            pattern = Prompt.ask("Pattern (eg: *.txt)", default="*")
            run(f'bulk-encrypt "{folder}" --pattern "{pattern}"')

        elif choice == 9:
            console.print("[bold green]Goodbye! Stay focused king 👑[/bold green]")
            break

        else:
            console.print("[bold red]Invalid choice. Try again.[/bold red]")


if __name__ == "__main__":
    main_menu()
