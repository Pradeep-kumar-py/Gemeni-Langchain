# download.py
import yt_dlp
import os
import base64
from PIL import Image
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from youtube_transcript_api._api import YouTubeTranscriptApi
from dotenv import load_dotenv  # type: ignore
load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


def download_audio_as_m4a(url, file="temp/audio.m4a"):
    ydl_opts = {
        "format": "bestaudio[ext=m4a]/bestaudio",  # Prefer m4a, fallback to best audio
        "outtmpl": file,
        "postprocessors": [],  # No FFmpeg needed, download as-is
        "quiet": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



# Ensure you have an audio file named 'example_audio.mp3' or provide the correct path.


def audio_transcription(audio_file_path):
    audio_file_path = "temp/audio.m4a"  # Path to your downloaded audio file
    audio_mime_type = "audio/mp4"
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found at {audio_file_path}")
    
    with open(audio_file_path, "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": "Transcribe the audio."},
            {
                "type": "media",
                "data": encoded_audio,  # Use base64 string directly
                "mime_type": audio_mime_type,
            },
        ]
    )
    response = llm.invoke([message])  # Uncomment to run
    print(f"Response for audio: {response.content}")
    return response.content
    



async def get_youtube_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([entry["text"] for entry in transcript_list])
    return transcript_text




