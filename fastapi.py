from fastapi import FastAPI
from pydantic import BaseModel
from model import converter

app = FastAPI()

class ImageRequest(BaseModel):
    image_url: str
    tags: list[str]

@app.post("/image-to-tags")
def convert_image(request: ImageRequest):
    result = converter(request.tags, request.image_url)
    return result
