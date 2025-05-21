import os
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import tempfile
from typing import List, Dict, Tuple, Any, Optional

# Load spaCy model for Italian
try:
    nlp = spacy.load("it_core_news_sm")
except OSError:
    # If model not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "it_core_news_sm"])
    nlp = spacy.load("it_core_news_sm")

# Mock classification model (in a real app, you'd train and save this)
# For demo purposes, we'll create a simple model with predefined categories
DOCUMENT_CATEGORIES = ["invoice", "contract", "letter", "report", "other"]

def mock_classifier():
    """Create a simple mock classifier for demonstration"""
    # This would normally be loaded from a saved model file
    vectorizer = TfidfVectorizer(max_features=1000)
    classifier = LogisticRegression()
    
    # Mock training data
    texts = [
        "fattura importo pagamento IVA totale", # invoice
        "contratto accordo parti firme clausole", # contract
        "gentile saluti cordiali distinti ringraziamenti", # letter
        "analisi dati risultati conclusioni grafici", # report
        "varie informazioni generiche contenuto", # other
    ]
    labels = [0, 1, 2, 3, 4]  # Corresponding to DOCUMENT_CATEGORIES
    
    # Fit the vectorizer and classifier
    X = vectorizer.fit_transform(texts)
    classifier.fit(X, labels)
    
    return vectorizer, classifier

# Initialize mock classifier
vectorizer, classifier = mock_classifier()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF using pdfplumber"""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def perform_ocr(file_path: str, language: str = "ita") -> str:
    """
    Perform OCR on a PDF or image file
    For PDFs, converts to images first
    """
    text = ""
    
    try:
        # Check if file is PDF
        if file_path.lower().endswith('.pdf'):
            # Convert PDF to images
            with tempfile.TemporaryDirectory() as temp_dir:
                images = convert_from_path(file_path)
                
                for i, image in enumerate(images):
                    # Save image temporarily
                    temp_img_path = os.path.join(temp_dir, f'page_{i}.png')
                    image.save(temp_img_path, 'PNG')
                    
                    # Perform OCR on the image
                    page_text = pytesseract.image_to_string(Image.open(temp_img_path), lang=language)
                    text += page_text + "\n\n"
        else:
            # Direct OCR for image files
            text = pytesseract.image_to_string(Image.open(file_path), lang=language)
            
        return text
    except Exception as e:
        print(f"Error performing OCR: {e}")
        return ""

def classify_document(text: str) -> Tuple[str, float]:
    """
    Classify the document based on its text content
    Returns the predicted class and confidence score
    """
    if not text or len(text.strip()) < 10:
        return "unknown", 0.0
    
    try:
        # Transform text using the vectorizer
        X = vectorizer.transform([text])
        
        # Get prediction and probability
        prediction = classifier.predict(X)[0]
        probabilities = classifier.predict_proba(X)[0]
        confidence = float(probabilities[prediction])
        
        return DOCUMENT_CATEGORIES[prediction], confidence
    except Exception as e:
        print(f"Error classifying document: {e}")
        return "unknown", 0.0

def extract_entities(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract named entities from text using spaCy
    Returns entities grouped by type
    """
    if not text or len(text.strip()) < 10:
        return {}
    
    try:
        doc = nlp(text)
        
        # Group entities by type
        entities_by_type = {}
        
        for ent in doc.ents:
            entity_type = ent.label_
            entity_text = ent.text
            entity_start = ent.start_char
            entity_end = ent.end_char
            
            if entity_type not in entities_by_type:
                entities_by_type[entity_type] = []
                
            entities_by_type[entity_type].append({
                "text": entity_text,
                "start": entity_start,
                "end": entity_end
            })
        
        return entities_by_type
    except Exception as e:
        print(f"Error extracting entities: {e}")
        return {}