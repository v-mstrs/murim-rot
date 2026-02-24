from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from .models import Base

sqlite_file_name = "murim.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    Base.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session
