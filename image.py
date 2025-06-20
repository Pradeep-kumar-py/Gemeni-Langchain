import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

# from IPython.display import Image, display
from PIL import Image
import io
import base64
from langchain_core.messages import AIMessage
from langchain_core.messages import BaseMessage  # Add this import
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-preview-image-generation")

message = {
    "role": "user",
    "content": "Generate a photorealistic image of a cuddly cat wearing a hat.",
}

response = llm.invoke(
    [message],
    generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
)


def _get_image_base64(response:BaseMessage) -> None:
    image_block = next(
        block
        for block in response.content
            if isinstance(block, dict) and block.get("image_url")
    )
    return image_block["image_url"].get("url").split(",")[-1]


image_base64 = _get_image_base64(response)
image_bytes = base64.b64decode(image_base64) # type: ignore
image = Image.open(io.BytesIO(image_bytes))
image.show()  # Display the image using the default image viewer












