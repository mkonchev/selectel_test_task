import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.logging import setup_logging
from app.services.parser import run_parse_job
from app.services.scheduler import create_scheduler

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск приложения")
    scheduler = create_scheduler(run_parse_job)
    scheduler.start()

    yield

    logger.info("Остановка приложения")
    if scheduler:
        scheduler.shutdown(wait=False)

app = FastAPI(title="Selectel Vacancies API", lifespan=lifespan)
app.include_router(api_router)

setup_logging()
