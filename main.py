from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import uvicorn  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from utils.types import ImageData
from controller.imageProcess import (
    process_image,
)


from dotenv import load_dotenv  # type: ignore

load_dotenv()


app = FastAPI()

origins = [
    "http://localhost:3000",  # Your Next.js frontend
    # Add production URL here if needed later
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from these origins
    allow_credentials=True,  # Allows cookies, sessions, etc.
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type, etc.)
)

# image_url = "https://www.bing.com/ck/a?!&&p=9b83700abb1a32ae9d81deaa8cde9ce233a7e449530d1d3cfc178f466849516dJmltdHM9MTc1MDM3NzYwMA&ptn=3&ver=2&hsh=4&fclid=3d3b609a-f775-604c-23ca-7425f60a61a1&u=a1L2ltYWdlcy9zZWFyY2g_cT1zb3BoaWUlMjB3b3JsZCUyMGJvb2slMjBpbWFnZSZGT1JNPUlRRlJCQSZpZD1EREFFNjg4Qzc2MjgyNDI1QTUxNTg4MzhFQkQ2OEQ1MTJGMkNERkEz&ntb=1"


@app.post("/process-image")
async def process_image_endpoint(image: ImageData):
    image_url = image.image_url
    summary = process_image(image_url)

    return JSONResponse(content={"summary": summary})


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Image Processing API"}


def main():
    print("Hello from testing-with-uv-python!")
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)


if __name__ == "__main__":
    main()
    print("Image processed successfully.")
