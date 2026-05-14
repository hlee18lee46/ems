import logging

from fastapi import FastAPI

from app.router.health import router as health_router
from app.router.employees import router as employees_router
from app.core.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:%(message)s"
)


def create_app() -> FastAPI:
    app = FastAPI(title="Employee Management System")
    app.state.settings = settings

    app.include_router(health_router)
    app.include_router(employees_router)

    return app


app = create_app()