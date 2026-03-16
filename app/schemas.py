from pydantic import BaseModel, Field

class NovelCreate(BaseModel):
    title: str
    slug: str

class NovelSummary(BaseModel):
    id: int
    title: str
    slug: str

class NovelCharacterView(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    highlight_color: str | None = None
    aliases: list[str] = Field(default_factory=list)

# NovelDetail inherits all fields from NovelSummary
# then addes one extra field: characters
class NovelDetail(NovelSummary):
    # Ensures every new object gets its own fresh, empty list 
    # instead of sharing one list across all objects (character: list[NovelCharacterView] = []).
    characters: list[NovelCharacterView] = Field(default_factory=list)

class CharacterCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    highlight_color: str | None = None
    aliases: list[str] = Field(default_factory=list)

class CharacterUpdate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None = None
    highlight_color: str | None = None
    aliases: list[str] = Field(default_factory=list)

class CharacterResponse(BaseModel):
    id: int
    novel_id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    highlight_color: str | None = None
    aliases: list[str] = Field(default_factory=list)

