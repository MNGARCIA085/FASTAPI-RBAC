from fastapi import FastAPI, APIRouter
from auth import router as auth_routes


app = FastAPI()


router = APIRouter()

app.include_router(auth_routes.router)
