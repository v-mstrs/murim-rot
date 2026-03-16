from sqlalchemy import create_engine, inspect, text
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
    with engine.begin() as connection:
        inspector = inspect(connection)
        character_columns = {column["name"] for column in inspector.get_columns("characters")}
        if "highlight_color" not in character_columns:
            connection.execute(
                text("ALTER TABLE characters ADD COLUMN highlight_color VARCHAR(32)")
            )

def get_db():
    with Session(engine) as session:
        yield session
