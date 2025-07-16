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










