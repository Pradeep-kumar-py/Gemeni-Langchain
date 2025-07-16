from youtube_transcript_api._api import YouTubeTranscriptApi
from dotenv import load_dotenv  # type: ignore
load_dotenv()


async def get_youtube_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = " ".join([entry["text"] for entry in transcript_list])
    return transcript_text