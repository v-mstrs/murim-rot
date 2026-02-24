from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class Novel(Base):
    __tablename__ = "novels"

    id: Mapped[int] = mapped_column(primary_key=True)

    slug: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String, nullable=False) 

    characters: Mapped[list[Character]] = relationship(
        back_populates="novel",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    novel_id: Mapped[int] = mapped_column(
        ForeignKey("novels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)


    novel: Mapped[Novel] = relationship(back_populates="characters")

    aliases: Mapped[list[CharacterAlias]] = relationship(
        back_populates="character",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # unique=True would make name unique globally.
    # We only want it unique per novel (novel_id + name).
    __table_args__ = (
        UniqueConstraint("novel_id", "name", name="uq_character_name_per_novel"),
    )


class CharacterAlias(Base):
    __tablename__ = "character_aliases"

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    alias: Mapped[str] = mapped_column(String, nullable=False)

    character: Mapped[Character] = relationship(back_populates="aliases")

    # Prevent duplicate aliases for the same character
    # (same alias can exist for different characters)
    __table_args__ = (
        UniqueConstraint("character_id", "alias", name="uq_character_alias"),
    )
