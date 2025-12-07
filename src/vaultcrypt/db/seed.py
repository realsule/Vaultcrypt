from vaultcrypt.db.session import SessionLocal, engine
from vaultcrypt.db.models import Base, User, Tag


def seed():
    Base.metadata.create_all(bind=engine)# Ensure tables exist
    db = SessionLocal()
    try:
         # Default user and tags
        if not db.query(User).filter_by(username='local').first():
            user = User(username='local')
            db.add(user)
        for name in ('personal', 'work', 'bank'):
            if not db.query(Tag).filter_by(name=name).first():
                db.add(Tag(name=name))
        db.commit()
    finally:
        db.close()

if __name__ == '__main__':
    seed()