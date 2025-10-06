from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import init_db, get_settings
from .routers import recipes as recipes_router
from .routers import menus as menus_router
from .seed import seed_data

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application with routes, CORS and startup events.
    Returns:
        FastAPI: Configured application instance.
    """
    settings = get_settings()
    app = FastAPI(
        title="Food Recipe API",
        description="Backend API for browsing, searching, and viewing recipes with images.",
        version="0.1.0",
        openapi_tags=[
            {"name": "recipes", "description": "Recipe browsing, search, and details"},
            {"name": "menus", "description": "Menu endpoints (sample)"},
        ],
    )

    # CORS setup
    allow_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()] if settings.CORS_ORIGINS else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(recipes_router.router, prefix="")
    app.include_router(menus_router.router, prefix="")

    @app.on_event("startup")
    async def on_startup():
        init_db()
        seed_data()

    @app.get("/", tags=["health"], summary="Health check", description="Simple health check endpoint.")
    def health():
        return {"status": "ok"}

    return app

app = create_app()
