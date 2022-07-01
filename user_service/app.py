from fastapi import FastAPI, status
from user_service.routes.user_settings_routes import router as UserSettingsRouter
from user_service.routes.user_routes import router as UsersRouter
from user_service.events import create_startup_handler, create_shutdown_handler
import logging

PREFIX = "/user"

# Create FastAPI app
app = FastAPI()

# Add Startup and Shutdown handlers
app.add_event_handler('startup', create_startup_handler(app))
app.add_event_handler('shutdown', create_shutdown_handler(app))

#Add User Settings router
app.include_router(UserSettingsRouter, prefix=PREFIX, tags=["User-Settings"])
app.include_router(UsersRouter, prefix=PREFIX, tags=["Users"])

#Create get endpoint for the root path
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}

#Create get endpoint for the health check
@app.get("/health")
def health_check():
    logging.log(logging.INFO, "Health check")
    return status.HTTP_200_OK
