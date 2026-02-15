from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import converter
from search import searcher

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class ImageRequest(BaseModel):
    image_url: str
    tags: list[str]


class SearchRequest(BaseModel):
    text: str
    year: int
    tags: list[str]


@app.post("/image-to-tags")
def convert_image(request: ImageRequest):
    result = converter(request.tags, request.image_url, debug=True)
    return result


@app.post("/search-tags")
def search_tags(request: SearchRequest):
    result = searcher(request.tags, request.text, request.year, debug=True)
    return result


@app.get("/")
def hello():
    return {"message": "Hello World"}
