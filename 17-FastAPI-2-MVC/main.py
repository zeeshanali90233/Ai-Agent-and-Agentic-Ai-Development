from fastapi import FastAPI
from routers.ai import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/v1", tags=["V1"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
