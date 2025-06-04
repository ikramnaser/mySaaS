# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install system dependencies needed for pdf2image
RUN apt-get update && apt-get install -y poppler-utils

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download Italian spaCy model
RUN python -m spacy download it_core_news_sm

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
