# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y poppler-utils

RUN python -m spacy download it_core_news_sm
RUN pip install fastapi uvicorn python-multipart aiofiles pillow pytesseract pdfplumber scikit-learn spacy


# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "back-main:app", "--host", "0.0.0.0", "--port", "8000"]
