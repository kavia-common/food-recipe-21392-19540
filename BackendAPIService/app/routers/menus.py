from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, schemas

router = APIRouter(tags=["menus"])

@router.get("/menus", response_model=schemas.MenuList, summary="List menus", description="Returns a list of menus.")
def list_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    return schemas.MenuList(items=[schemas.Menu.model_validate(m) for m in menus])
