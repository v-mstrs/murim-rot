from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.schemas import (
    CharacterCreate,
    CharacterResponse,
    NovelCharacterView,
    NovelCreate,
    NovelDetail,
    NovelSummary,
)
from .models import CharacterAlias, Novel, Character
from .database import create_db_and_tables, get_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database initialized")
    yield

app = FastAPI(lifespan=lifespan)

# const response = await fetch("http://127.0.0.1:8000/novels");
# const novels = await response.json();
# console.log(novels.map(n => n.slug));

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/novels")
def list_novels(db: Session = Depends(get_db)):
    return db.scalars(select(Novel)).all()

@app.get("/novels/{slug}", response_model=NovelDetail)
def get_novel(slug: str, db: Session = Depends(get_db)):
    novel = db.execute(
        select(Novel)
        .where(Novel.slug == slug)
        # load characters and their aliases in optimized follow-up queries
        .options(selectinload(Novel.characters).selectinload(Character.aliases))
    ).scalar_one_or_none()
    
    if not novel:
        raise HTTPException(404, "Novel not found.")

    return NovelDetail(
        id=novel.id,
        title=novel.title,
        slug=novel.slug,
        characters=[
            NovelCharacterView(
                name=char.name,
                description=char.description,
                image_url=char.image_url,
                highlight_color=char.highlight_color,
                aliases=[a.alias for a in char.aliases],
            )
            for char in novel.characters
        ],
    )

@app.post("/novels/{slug}/characters", response_model=CharacterResponse)
def add_character(slug: str, character: CharacterCreate, db: Session = Depends(get_db)):
    novel = db.execute(
        select(Novel)
        .where(Novel.slug == slug)
    ).scalar_one_or_none()

    if not novel:
        raise HTTPException(404, "Novel not found.")

    new_char = Character(
        name = character.name,
        description = character.description,
        image_url = character.image_url,
        highlight_color = character.highlight_color,
        novel_id = novel.id,
    )

    new_char.aliases = [
        CharacterAlias(alias=a.strip()) for a in character.aliases if a.strip()
    ]

    db.add(new_char)
    db.commit()
    db.refresh(new_char)

    return CharacterResponse(
        id=new_char.id,
        novel_id=new_char.novel_id,
        name=new_char.name,
        description=new_char.description,
        image_url=new_char.image_url,
        highlight_color=new_char.highlight_color,
        aliases=[a.alias for a in new_char.aliases],
    )

@app.post("/", response_model=NovelSummary)
def add_novel(payload: NovelCreate, db: Session = Depends(get_db)):
    novel = Novel(
        title = payload.title,
        slug  = payload.slug
    )
    
    existing = db.execute(
        select(Novel).where(Novel.slug == payload.slug)
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(400, "Novel with this slug already exists")
    
    db.add(novel)
    db.commit()
    db.refresh(novel)

    return novel


