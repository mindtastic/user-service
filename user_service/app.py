from fastapi import FastAPI, status
from user_service.routes.user_routes import router as UsersRouter
from user_service.events import create_startup_handler, create_shutdown_handler
from loguru import logger

# Create FastAPI app
app = FastAPI()

# Add Startup and Shutdown handlers
app.add_event_handler('startup', create_startup_handler(app))
app.add_event_handler('shutdown', create_shutdown_handler(app))

#Add User Settings router
app.include_router(UsersRouter, tags=["Users"])

#Create get endpoint for the root path
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}

#Create get endpoint for the health check
@app.get("/health")
def health_check():
    logger.info("Health check")
    return status.HTTP_200_OK
