from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, Table, ForeignKey
import datetime

Base = declarative_base()

entry_tags = Table(
    'entry_tags', Base.metadata,
    Column('entry_id', Integer, ForeignKey('vault_entries.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    entries = relationship('VaultEntry', back_populates='owner')
    audits = relationship('AuditLog', back_populates='user')

    def to_dict(self):
        return {'id': self.id, 'username': self.username, 'created_at': self.created_at.isoformat()}

class VaultEntry(Base):
    __tablename__ = 'vault_entries'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    username = Column(String, nullable=True)
    password = Column(Text, nullable=False)  # encrypted bytes stored as b64
    notes = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    owner = relationship('User', back_populates='entries')
    tags = relationship('Tag', secondary=entry_tags, back_populates='entries')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'username': self.username,
            'notes': self.notes,
            'owner_id': self.owner_id,
            'tags': [t.name for t in self.tags],
            'created_at': self.created_at.isoformat()
        }

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    entries = relationship('VaultEntry', secondary=entry_tags, back_populates='tags')

    def __repr__(self):
        return f'<Tag {self.name}>'

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String, nullable=False)
    details = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', back_populates='audits')

    def to_tuple(self):
        return (self.id, self.user_id, self.action, self.created_at.isoformat())