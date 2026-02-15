from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model import converter

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


@app.post("/image-to-tags")
def convert_image(request: ImageRequest):
    result = converter(request.tags, request.image_url)
    return result


@app.get("/")
def hello():
    return {"message": "Hello World"}
