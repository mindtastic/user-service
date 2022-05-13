import os
from fastapi import FastAPI, HTTPException
import motor.motor_asyncio


app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"], tls=True, tlsAllowInvalidCertificates=True)
db = client.user_service


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/{id}", response_description="Get a single user", response_model=UserModel
)
async def show_user(id: str):
    if (user := await db["user"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"User {id} not found")