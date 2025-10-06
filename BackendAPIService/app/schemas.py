from typing import List, Optional
from pydantic import BaseModel, Field

class Image(BaseModel):
    id: int = Field(..., description="Image ID")
    url: str = Field(..., description="Public URL for the image")
    alt: Optional[str] = Field(None, description="Alt text")

    class Config:
        from_attributes = True

class RecipeBase(BaseModel):
    title: str = Field(..., description="Recipe title")
    description: Optional[str] = Field(None, description="Short description")

class Recipe(RecipeBase):
    id: int = Field(..., description="Recipe ID")
    ingredients: List[str] = Field(default_factory=list, description="List of ingredients")
    instructions: List[str] = Field(default_factory=list, description="List of steps")
    images: List[Image] = Field(default_factory=list, description="Images for the recipe")

    class Config:
        from_attributes = True

class RecipeList(BaseModel):
    items: List[Recipe] = Field(default_factory=list, description="List of recipes")

class Menu(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

class MenuList(BaseModel):
    items: List[Menu] = Field(default_factory=list)
