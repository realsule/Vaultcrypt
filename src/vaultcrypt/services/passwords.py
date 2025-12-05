import secrets
import string
from typing import List
from vaultcrypt.services.encryption import encrypt_bytes, decrypt_bytes
from vaultcrypt.db.session import SessionLocal
from vaultcrypt.db import models


def generate_password(length: int = 16, use_symbols: bool = True) -> str:
    alphabet = string.ascii_letters + string.digits
    if use_symbols:
        alphabet += '!@#$%^&*()-_=+[]{};:,.<>?'
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def add_entry(title: str, username: str | None, password_plain: str, owner: str = 'local', tags: List[str] | None = None):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == owner).first()
        if not user:
            user = models.User(username=owner)
            db.add(user)
            db.commit()
            db.refresh(user)
        enc = encrypt_bytes(password_plain.encode('utf-8'))
        entry = models.VaultEntry(title=title, username=username, password=enc.decode('utf-8'), owner=user)
        if tags:
            tag_objs = []
            for t in tags:
                ex = db.query(models.Tag).filter(models.Tag.name == t).first()
                if not ex:
                    ex = models.Tag(name=t)
                    db.add(ex)
                    db.commit()
                tag_objs.append(ex)
            entry.tags = tag_objs
        db.add(entry)
        db.commit()
        db.refresh(entry)
        db.add(models.AuditLog(user_id=user.id, action='add', details=f'entry:{entry.id}'))
        db.commit()
        return entry
    finally:
        db.close()


def get_entry(entry_id: int, reveal: bool = False):
    db = SessionLocal()
    try:
        entry = db.query(models.VaultEntry).get(entry_id)
        if not entry:
            return None
        data = entry.to_dict()
        if reveal:
            # stored as string of bytes, get bytes back
            pwd = entry.password.encode('utf-8')
            data['password'] = decrypt_bytes(pwd).decode('utf-8')
        return data
    finally:
        db.close()


def list_entries(owner: str | None = None, tag: str | None = None):
    db = SessionLocal()
    try:
        q = db.query(models.VaultEntry)
        if owner:
            q = q.join(models.User).filter(models.User.username == owner)
        if tag:
            q = q.join(models.VaultEntry.tags).filter(models.Tag.name == tag)
        return [e.to_dict() for e in q.order_by(models.VaultEntry.created_at.desc()).all()]
    finally:
        db.close()


def remove_entry(entry_id: int):
    db = SessionLocal()
    try:
        e = db.query(models.VaultEntry).get(entry_id)
        if not e:
            return False
        db.delete(e)
        db.commit()
        db.add(models.AuditLog(user_id=e.owner_id, action='delete', details=f'entry:{entry_id}'))
        db.commit()
        return True
    finally:
        db.close()