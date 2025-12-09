from .db.session import engine
from .db.models import Base

def main():
    print("Creating tables...")
    Base.metadata.create_all(engine) #create all models/tables
    print("Database initialized successfully.")

if __name__ == "__main__":
    main()
