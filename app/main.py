import logging
import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.config.logs.log_config import LOGGING_CONFIG
from app.config.settings import settings

# Set up logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(title="DevelopersToday Test Task")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)
