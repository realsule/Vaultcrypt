# VaultCrypt CLI — Encrypted Vault & File Manager

VaultCrypt is a Python CLI app that lets you **securely store passwords and encrypt files** while showing motivational quotes. Built with **SQLAlchemy**, **Typer**, and **Fernet encryption**.

---

## Features

- Add, list, view, and delete password entries
- Auto-generate strong passwords
- Encrypt/decrypt individual files
- Bulk encrypt all files in a folder
- Motivational quotes after every action
- Secure storage with SQLAlchemy ORM 

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd vaultcrypt

pip install pipenv

pipenv install

pipenv shell

```

### Setup

Environment variables (important)

Before you store or read passwords, set a master encryption key. This key is required to encrypt/decrypt passwords in the database:

### 1. Generate MASTER_KEY for encryption

```bash
python - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY

export MASTER_KEY="<PASTE_KEY_HERE>"
## Initialize the database (creates tables)
python -m vaultcrypt.initdb

python -m vaultcrypt.cli --help
```

### 2. if you prefer CLI with menu

```bash
## Initialize the database (creates tables)
    python -m vaultcrypt.initdb

##Start the interactive menu
    python -m vaultcrypt.menu
```
