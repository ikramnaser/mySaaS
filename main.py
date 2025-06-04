import os
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uuid
from typing import List, Dict, Any
import tempfile

# Import processing modules
from document_processor import (
    extract_text_from_pdf,
    perform_ocr,
    classify_document,
    extract_entities
)

app = FastAPI(title="Document Processing API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for uploads if it doesn't exist
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static files (frontend)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload and process a document (PDF or image)
    """
    # Validate file type
    allowed_extensions = [".pdf", ".png", ".jpg", ".jpeg"]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type not supported. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Create unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    try:
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the document
        result = process_document(file_path, file_ext)
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return JSONResponse(content=result)
    
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

def process_document(file_path: str, file_ext: str) -> Dict[str, Any]:
    """
    Process the document through the entire pipeline:
    1. Text extraction (PDF parsing or OCR)
    2. Document classification
    3. Named entity recognition
    """
    # Step 1: Extract text
    if file_ext == ".pdf":
        # Try to extract text directly first
        text = extract_text_from_pdf(file_path)
        
        # If no text was extracted, it might be a scanned PDF
        if not text or len(text.strip()) < 50:  # Arbitrary threshold
            text = perform_ocr(file_path, language="ita")
    else:
        # For images, always use OCR
        text = perform_ocr(file_path, language="ita")
    
    # Step 2: Classify document
    doc_class, confidence = classify_document(text)
    
    # Step 3: Extract entities
    entities = extract_entities(text)
    
    # Return structured results
    return {
        "text": text[:1000] + "..." if len(text) > 1000 else text,  # Truncate long texts
        "classification": {
            "label": doc_class,
            "confidence": confidence
        },
        "entities": entities,
        "status": "success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)