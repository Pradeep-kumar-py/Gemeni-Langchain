# Use official Python image
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies using uv sync
RUN uv sync --frozen --no-dev

# Copy the rest of the project files
COPY . .
COPY .env .env

# Expose the port FastAPI will run on
EXPOSE 80

# Run the FastAPI server
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]