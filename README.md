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
git clone <git@github.com:realsule/Vaultcrypt.git>
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

export MASTER_KEY="<0nI_Z6omslomEr2_F29oYW10y73qm3Vyxr_DnEUCsjM=>"
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
### 3. if you prefer CLI with no menu
```bash
#Use the Typer CLI directly, for example:
#Initialize DB:

python -m vaultcrypt.cli init --sample

#Generate a password:

python -m vaultcrypt.cli generate-password --length 20 --symbols

#Add an entry (store a password):

python -m vaultcrypt.cli add-entry --title "Gmail" --username "you@gmail.com" --password "mypassword" --tag personal --owner local

#List entries:

python -m vaultcrypt.cli list-entries --owner local


#View one entry (reveal password):

python -m vaultcrypt.cli get-entry 1 --reveal


#Encrypt a file:

python -m vaultcrypt.cli encrypt-file path/to/file --key filekey.key


#Decrypt a file:

python -m vaultcrypt.cli decrypt-file path/to/file.enc --key filekey.key


#Bulk encrypt a folder:

python -m vaultcrypt.cli bulk-encrypt ./documents --pattern '*.txt'

##Generates New encrypted Key:

python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'
```