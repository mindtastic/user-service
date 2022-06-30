from typing import Callable
from fastapi import FastAPI

from user_service.database import connect_to_mongodb

def create_startup_handler(app: FastAPI) -> Callable:
    async def startup_handler() -> None:
        await connect_to_mongodb(app)

    return startup_handler

def create_shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown_handler() -> None:
        pass

    return shutdown_handler
