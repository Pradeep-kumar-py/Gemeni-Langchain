import os
import base64
import uuid
from google import genai
from google.genai import types
import wave
from PIL import Image
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv  
load_dotenv()

from google.cloud import texttospeech

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


def process_image(image_url, title):
    if not image_url:
        raise ValueError("Image path cannot be empty")

    full_prompt = f"""
                You are a creative literary assistant with a keen eye for detail. Your task is to imagine and write a compelling summary of a book based only on its cover.

                The book's title is: "{title}".

                Examine the book’s title, subtitle, author name, and visual design—including colors, typography, artwork, and overall mood. Based on these, craft an engaging and imaginative long-form summary that captures what this book might be about.

                Do not refer to the image directly or mention that you're interpreting a cover. Simply write the summary as if you already knew the story. Be descriptive, vivid, and coherent, as if pitching the book to a reader who might buy it.
                """

    message_url = HumanMessage(
        content=[
            {
                "type": "text",
                "text": full_prompt,
            },
            {
                "type": "image_url",
                "image_url": image_url,
            },
        ]
    )

    result_url = llm.invoke([message_url])
    return result_url.content









def audio_summary(summary):
    print("Summary to be converted:", summary)

    def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(pcm)

    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=f"Read this cheerfully: {summary}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore',
                    )
                )
            )
        )
    )

    data = response.candidates[0].content.parts[0].inline_data.data  # type: ignore

    file_name = 'summary_output.wav'
    wave_file(file_name, data)
    print(f"Audio saved as {file_name}")

    print("Summary to be converted:", summary)

    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text="hii i am pradeep kumar")

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        
    print('Audio content written to "output.mp3"')
    
    return "output.mp3"