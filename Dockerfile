# Use official Python image
FROM python:3.13-slim

# Set workdir
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency definitions
COPY pyproject.toml uv.lock ./

# Install dependencies
# This layer is cached and only runs again if dependency files change
RUN uv pip install --system .

# Copy the rest of the project files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI server
# Corrected "app.main:app" to "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]