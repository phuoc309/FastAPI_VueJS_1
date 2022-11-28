from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import books

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def root_access():
#     return {"message": "Hello World"}


app.include_router(books.router)