from fastapi import FastAPI
from app.view import numbers

app = FastAPI(title="Byne Challenge API")

app.include_router(numbers.router, prefix="/numbers")
