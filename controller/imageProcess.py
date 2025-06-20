import os
import base64
from PIL import Image
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
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

prompt_text = """
You are a helpful assistant trained to generate a summary of a book using only the cover image. 
Analyze the title, subtitle, author name, design, and visual elements.

Based on these, write a long and creative summary of what this book might be about. 
Do not say "based on the image" — just write the summary directly.
"""


def process_image(image_url):
    if not image_url:
        raise ValueError("Image path cannot be empty")

    message_url = HumanMessage(
        content=[
            {
                "type": "text",
                "text": prompt_text,
            },
            {
                "type": "image_url",
                "image_url": image_url,
            },
        ]
    )

    result_url = llm.invoke([message_url])
    return result_url.content
