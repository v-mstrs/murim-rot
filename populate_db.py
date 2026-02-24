from sqlalchemy.orm import Session
from .database import engine, create_db_and_tables
from .models import Novel, Character

def seed_db():
    create_db_and_tables()

    with Session(engine) as db:
        novel = Novel(
            slug = "bad-born-blood",
            title= "Bad Born Blood"
        )

        character = Character(name="John", description="fat loser", novel=novel)

        db.add(novel)
        db.add(character)
        db.commit()

if __name__ == "__main__":
    seed_db()
