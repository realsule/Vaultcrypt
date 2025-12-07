import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_cli_command(command_list):
    """Run a CLI command and stream output."""
    try:
        subprocess.run(["python", "-m", "vaultcrypt.cli"] + command_list, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Command failed:[/red] {e}")

def main():
    while True:
        console.print(Panel.fit(
            """
🔐 [bold cyan]VAULTCRYPT INTERACTIVE MENU[/bold cyan]

1. Generate Password
2. Add Password Entry
3. List Entries
4. View Entry
5. Remove Entry
6. Encrypt File
7. Decrypt File
8. Bulk Encrypt Folder
9. Exit
""", title="🔐 Vaultcrypt"))

        choice = input("Choose an option: ").strip()

        if choice == "1":
            length = input("Password length (default 16): ").strip()
            args = ["generate-password"]
            if length:
                args += ["--length", length]
            run_cli_command(args)

        elif choice == "2":
            title = input("Title: ")
            username = input("Username: ")
            password = input("Password (leave blank to auto-generate): ")
            args = ["add-entry", "--title", title, "--username", username]
            if password:
                args += ["--password", password]
            run_cli_command(args)

        elif choice == "3":
            run_cli_command(["list-entries"])

        elif choice == "4":
            entry_id = input("Entry ID: ")
            reveal = input("Reveal password? (y/n): ").lower() == "y"
            args = ["get-entry", "--id", entry_id]
            if reveal:
                args.append("--reveal")
            run_cli_command(args)

        elif choice == "5":
            entry_id = input("Entry ID to remove: ")
            run_cli_command(["remove-entry", "--id", entry_id])

        elif choice == "6":
            path = input("Path of file to encrypt: ")
            run_cli_command(["encrypt-file", "--path", path])

        elif choice == "7":
            path = input("Path of file to decrypt: ")
            run_cli_command(["decrypt-file", "--path", path])

        elif choice == "8":
            folder = input("Folder path: ")
            pattern = input("Glob pattern (e.g. *.txt): ")
            run_cli_command(["bulk-encrypt", "--folder", folder, "--pattern", pattern])

        elif choice == "9":
            console.print("[green]Goodbye! Stay focused king 👑[/green]")
            break

        else:
            console.print("[red]Invalid choice, try again.[/red]")


if __name__ == "__main__":
    main()
