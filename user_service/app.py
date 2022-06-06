from fastapi import FastAPI, status
from user_service.routes.user_settings_routes import router as UserSettingsRouter
from user_service.routes.user_routes import router as UsersRouter

PREFIX = "/user"

# Create FastAPI app
app = FastAPI()

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
    status.HTTP_200_OK