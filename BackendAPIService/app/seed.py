from sqlalchemy.orm import Session
from .db import get_db, _engine_and_session
from . import models

def _seed(db: Session):
    if db.query(models.Recipe).count() > 0:
        return

    # Sample recipes
    pancakes = models.Recipe(
        title="Classic Pancakes",
        description="Fluffy pancakes perfect for breakfast.",
        ingredients="Flour\nEggs\nMilk\nSugar\nBaking powder\nSalt\nButter",
        instructions="Mix dry ingredients.\nWhisk in wet ingredients.\nCook on griddle until golden.\nServe with syrup.",
    )
    pancakes.images = [
        models.Image(url="https://images.unsplash.com/photo-1551024709-8f23befc6cf7?w=1200", alt="Pancakes"),
        models.Image(url="https://images.unsplash.com/photo-1495214783159-3503fd1b572d?w=1200", alt="Stack of pancakes"),
    ]

    salad = models.Recipe(
        title="Mediterranean Salad",
        description="Crisp veggies with feta and olives.",
        ingredients="Tomatoes\nCucumbers\nRed onion\nFeta cheese\nOlives\nOlive oil\nLemon juice\nOregano\nSalt\nPepper",
        instructions="Chop vegetables.\nCombine and toss with dressing.\nTop with feta and olives.",
    )
    salad.images = [
        models.Image(url="https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=1200", alt="Fresh salad")
    ]

    pasta = models.Recipe(
        title="Creamy Mushroom Pasta",
        description="Rich and savory pasta with mushrooms.",
        ingredients="Pasta\nMushrooms\nGarlic\nCream\nParmesan\nButter\nSalt\nPepper\nParsley",
        instructions="Cook pasta.\nSauté mushrooms and garlic.\nAdd cream and cheese.\nCombine with pasta and serve.",
    )
    pasta.images = [
        models.Image(url="https://images.unsplash.com/photo-1525755662778-989d0524087e?w=1200", alt="Mushroom pasta")
    ]

    menu = models.Menu(name="Brunch Favorites", description="Perfect weekend picks.")

    pancakes.menus.append(menu)
    salad.menus.append(menu)

    db.add_all([pancakes, salad, pasta, menu])
    db.commit()

# PUBLIC_INTERFACE
def seed_data():
    """Seed initial data if database is empty."""
    _, SessionLocal = _engine_and_session()
    with SessionLocal() as db:
        _seed(db)
