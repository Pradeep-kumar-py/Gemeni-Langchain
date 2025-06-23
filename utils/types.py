from pydantic import BaseModel
from typing import List, Optional

class ImageData(BaseModel):
    image_url:str
    title: Optional[str] = None

class AudioData(BaseModel):
    audio_url: str

class VideoData(BaseModel):
    video_id: str
    
    
class VideoRequest(BaseModel):
    video_url: str
    
class AudioSummary(BaseModel):
    summary: str