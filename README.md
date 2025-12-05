# VaultCrew CLI — Encrypted Vault & File Manager

VaultCrew is a Python CLI app that lets you **securely store passwords and encrypt files** while showing motivational quotes. Built with **SQLAlchemy**, **Typer**, and **Fernet encryption**.

---

## Features

- Add, list, view, and delete password entries
- Auto-generate strong passwords
- Encrypt/decrypt individual files
- Bulk encrypt all files in a folder
- Motivational quotes after every action
- Secure storage with SQLAlchemy ORM (3+ tables: User, VaultEntry, Tag)
- CLI designed with Typer for smooth command-line experience

---

## 🛠 Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd vaultcrew

pip install pipenv

pipenv install
pipenv install --dev pytest

pipenv shell

```

### Setup

1. Generate MASTER_KEY for encryption

python - <<'PY'
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
PY

export MASTER_KEY="<PASTE_KEY_HERE>"


python -m vaultcrew.cli init --sample
