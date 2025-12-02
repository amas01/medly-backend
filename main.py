from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from medly_backend.api.health import router as health_router
from medly_backend.api.users import router as users_router
from medly_backend.api.lessons import router as lessons_router
from medly_backend.api.papers import router as papers_router
from medly_backend.api.items import router as items_router


def get_application() -> FastAPI:
    app = FastAPI(
        title="Medly API",
        version="1.0.0",
        description="Curriculum, assessment, and learner activity API",
    )

    # --- Register routers ---
    app.include_router(health_router, tags=["Health"])
    app.include_router(users_router, tags=["Users"])
    app.include_router(lessons_router, tags=["Lessons"])
    app.include_router(papers_router, tags=["Papers"])
    app.include_router(items_router, tags=["Items"])

    return app


app = get_application()
