from pydantic import BaseModel
from typing import List, Optional

class ImageData(BaseModel):
    image_url:str

