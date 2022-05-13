from fastapi import FastAPI
from user_service.routes.user_settings import router as UserSettingsRouter

# Create FastAPI app
app = FastAPI()

#Add User Settings router  
app.include_router(UserSettingsRouter, prefix="/user-settings", tags=["User-Settings"])

#Create get endpoint for the root path
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Hello World"}
