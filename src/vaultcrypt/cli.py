#!/usr/bin/env python3
import typer
from typing import Optional, List
from vaultcrypt.db import session as db_s
from vaultcrypt.db import models
from vaultcrypt.services import passwords, files, quotes
from vaultcrypt.utils import show_quote
from vaultcrypt.db.seed import seed
from vaultcrypt.logger import logger

app = typer.Typer() # CLI app instance(main entry point for vaultcrypt commands)

@app.command()
def init(sample: bool = typer.Option(False, '--sample')):
    """Initialize DB and optional seed."""
    models.Base.metadata.create_all(bind=db_s.engine)
    if sample:
        seed()# Optionally seed with sample data
    typer.echo('Initialized DB')
    show_quote(quotes.random_quote())


@app.command()
def gen_file_key(path: Optional[str] = typer.Option(None, '--out')):
    """Generate and save a file encryption key."""
    k = files.generate_file_key(path) # Create file key
    typer.echo(f'Wrote file key to {path or files.FILE_KEY_PATH if hasattr(files, "FILE_KEY_PATH") else "default path"}')
    show_quote(quotes.random_quote())


@app.command()
def encrypt_file(path: str, keyfile: Optional[str] = typer.Option(None, '--key')):
    """Encrypt a file with the file key."""
    key = None
    if keyfile:
        key = open(keyfile, 'rb').read()
    out = files.encrypt_file(path, key)# Encrypt the file
    typer.echo(f'Encrypted -> {out}')
    show_quote(quotes.random_quote())


@app.command()
def decrypt_file(path: str, keyfile: Optional[str] = typer.Option(None, '--key')):
    """Decrypt a file encrypted with the file key."""
    key = None
    if keyfile:
        key = open(keyfile, 'rb').read()
    out = files.decrypt_file(path, key)# Decrypt the file
    typer.echo(f'Decrypted -> {out}')
    show_quote(quotes.random_quote())


@app.command()
def bulk_encrypt(folder: str, pattern: str = typer.Option('*', '--pattern')):
    """Encrypt all files in a folder matching a glob pattern."""
    outs = files.bulk_encrypt_folder(folder, pattern=pattern)# Encrypt folder by pattern
    typer.echo(f'Encrypted {len(outs)} files')
    show_quote(quotes.random_quote())


@app.command()
def generate_password(length: int = typer.Option(16, '--length'), symbols: bool = typer.Option(True, '--symbols')):
    """Generate a secure password and print it."""
    pwd = passwords.generate_password(length=length, use_symbols=symbols)
    typer.echo(pwd)
    show_quote(quotes.random_quote())


@app.command()
def add_entry(title: str = typer.Option(..., '--title'), username: Optional[str] = typer.Option(None, '--username'), password: Optional[str] = typer.Option(None, '--password'), owner: str = typer.Option('local', '--owner'), tags: Optional[List[str]] = typer.Option(None, '--tag')):
    """Add a vault entry. If password omitted it will be generated."""
    if not password:
        password = passwords.generate_password()# Auto-generate password if not provided
    entry = passwords.add_entry(title=title, username=username, password_plain=password, owner=owner, tags=tags)
    typer.echo(f'Added entry id={entry.id} title={entry.title}')
    show_quote(quotes.random_quote())


@app.command()
def get_entry(entry_id: int, reveal: bool = typer.Option(False, '--reveal')):
    """Get entry metadata. Use --reveal to see password."""
    data = passwords.get_entry(entry_id, reveal=reveal)
    if not data:
        raise typer.Exit(code=1, message='Entry not found')
    typer.echo(data)
    show_quote(quotes.random_quote())


@app.command()
def list_entries(owner: Optional[str] = typer.Option(None, '--owner'), tag: Optional[str] = typer.Option(None, '--tag')):
    rows = passwords.list_entries(owner=owner, tag=tag)
    typer.echo(rows)
    show_quote(quotes.random_quote())


@app.command()
def remove_entry(entry_id: int, confirm: bool = typer.Option(False, '--confirm')):
    if not confirm:
        raise typer.Exit(code=1, message='Add --confirm to delete')
    ok = passwords.remove_entry(entry_id)
    if ok:
        typer.echo('Deleted')
        show_quote(quotes.random_quote())
    else:
        raise typer.Exit(code=1, message='Entry not found')


if __name__ == '__main__':
    app()