from typing import List
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

# Association table for many-to-many between Recipe and Menu
recipe_menu = Table(
    "recipe_menu",
    Base.metadata,
    Column("recipe_id", ForeignKey("recipes.id"), primary_key=True),
    Column("menu_id", ForeignKey("menus.id"), primary_key=True),
)

class Recipe(Base):
    """Recipe model."""
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    ingredients: Mapped[str | None] = mapped_column(Text, nullable=True)  # stored as newline-separated
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)  # stored as newline-separated

    images: Mapped[List["Image"]] = relationship("Image", back_populates="recipe", cascade="all, delete-orphan")
    menus: Mapped[List["Menu"]] = relationship("Menu", secondary=recipe_menu, back_populates="recipes")

class Image(Base):
    """Image model associated with a recipe."""
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(500))
    alt: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recipe_id: Mapped[int] = mapped_column(Integer, ForeignKey("recipes.id"))
    recipe: Mapped["Recipe"] = relationship("Recipe", back_populates="images")

class Menu(Base):
    """Menu model grouping multiple recipes."""
    __tablename__ = "menus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    recipes: Mapped[List["Recipe"]] = relationship("Recipe", secondary=recipe_menu, back_populates="menus")
