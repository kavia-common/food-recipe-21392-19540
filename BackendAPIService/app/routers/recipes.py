from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(tags=["recipes"])

def _split_lines(value: str | None) -> List[str]:
    return [line.strip() for line in (value or "").splitlines() if line.strip()]

def _to_schema_recipe(r: models.Recipe) -> schemas.Recipe:
    return schemas.Recipe(
        id=r.id,
        title=r.title,
        description=r.description,
        ingredients=_split_lines(r.ingredients),
        instructions=_split_lines(r.instructions),
        images=[schemas.Image.model_validate(img) for img in r.images],
    )

@router.get("/recipes", response_model=schemas.RecipeList, summary="List recipes", description="Returns a list of recipes.")
def list_recipes(db: Session = Depends(get_db)):
    items = db.query(models.Recipe).all()
    return schemas.RecipeList(items=[_to_schema_recipe(r) for r in items])

@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe, summary="Get recipe by ID", description="Return a single recipe by its ID.")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    r = db.get(models.Recipe, recipe_id)
    if not r:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return _to_schema_recipe(r)

@router.get("/search", response_model=schemas.RecipeList, summary="Search recipes", description="Search recipes by title or ingredient using query parameter q.")
def search_recipes(q: str = Query("", description="Search query"), db: Session = Depends(get_db)):
    if not q:
        items = db.query(models.Recipe).all()
        return schemas.RecipeList(items=[_to_schema_recipe(r) for r in items])

    q_lower = f"%{q.lower()}%"
    # Simple LIKE-based search against title or description
    matches = (
        db.query(models.Recipe)
        .filter(
            (models.Recipe.title.ilike(q_lower))
            | (models.Recipe.description.ilike(q_lower))
            | (models.Recipe.ingredients.ilike(q_lower))
        )
        .all()
    )
    return schemas.RecipeList(items=[_to_schema_recipe(r) for r in matches])
