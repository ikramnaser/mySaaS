# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy all files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn python-multipart aiofiles pillow pytesseract pdfplumber scikit-learn spacy

RUN python -m spacy download it_core_news_sm

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "back-main:app", "--host", "0.0.0.0", "--port", "8000"]
