from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from utils.types import (ImageData, AudioData, VideoData, AudioSummary)
from controller.imageProcess import (
    process_image,
    audio_summary
)
from controller.audioProcess import (
    download_audio_as_m4a,
    audio_transcription,
    get_youtube_transcript
)


from dotenv import load_dotenv  # type: ignore

load_dotenv()


app = FastAPI()

# origins = [
#     "http://localhost:3000",  # Your Next.js frontend
#     # Add production URL here if needed later
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from these origins
    allow_credentials=True,  # Allows cookies, sessions, etc.
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)




# download_audio_as_m4a(url)

@app.post("/transcribe-youtube")
async def transcribe_youtube(video: VideoData):
    video_id = video.video_id
    if not video_id:
        return JSONResponse(status_code=400, content={"error": "Video ID cannot be empty"})
    try:
        transcript = await get_youtube_transcript(video_id) # type: ignore
        return JSONResponse(content={"transcript": transcript})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})





@app.post("/process-image")
async def process_image_endpoint(image: ImageData):
    image_url = image.image_url
    title = image.title
    summary = process_image(image_url, title)
    # audio_summary(summary)
    return JSONResponse(content={"summary": summary})


@app.post("/audio_summary")
async def audio_summary_endpoint(data: AudioSummary):
    summary = data.summary    
    audio_summary(summary)
    return {"audio_url": f"/static/"}





@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI server!"}







def main():
    print("Hello from testing-with-uv-python!")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)





if __name__ == "__main__":
    main()
    print("Image processed successfully.")
