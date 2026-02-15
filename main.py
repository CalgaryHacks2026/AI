from pydantic import BaseModel

from main import FastAPI
from model import converter

app = FastAPI()


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
