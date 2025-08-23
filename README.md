# 📄 Document Processing SaaS Platform

> A full-stack intelligent document processing platform that transforms PDFs and images into structured data using AI/ML technologies.

## 🚀 Overview

This project demonstrates a production-ready SaaS platform that automatically processes documents using advanced AI/ML techniques. The system extracts text from PDFs and images, classifies documents by type, and identifies named entities - all through an intuitive web interface.

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/JSON    ┌──────────────────┐
│   Frontend      │ ◄──────────────► │   FastAPI        │
│   (HTML/JS)     │                  │   Backend        │
└─────────────────┘                  └──────────────────┘
                                              │
                                              ▼
                                    ┌──────────────────┐
                                    │  Processing      │
                                    │  Pipeline        │
                                    │                  │
                                    │ • PDF Parser     │
                                    │ • OCR Engine     │
                                    │ • ML Classifier  │
                                    │ • NER Extractor  │
                                    └──────────────────┘
```

## ✨ Key Features

- **Intelligent Text Extraction**: Handles both text-based and scanned PDFs using OCR
- **Document Classification**: ML-powered categorization (invoices, contracts, letters, reports)
- **Named Entity Recognition**: Extracts people, organizations, dates, and monetary values
- **Multi-language Support**: Optimized for Italian text processing
- **Responsive UI**: Modern drag-and-drop interface with real-time progress
- **Production Ready**: Containerized with Docker for easy deployment

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **spaCy** - Advanced NLP library for entity recognition
- **Tesseract OCR** - Optical character recognition engine
- **scikit-learn** - Machine learning for document classification
- **pdfplumber** - PDF text extraction and parsing
- **pdf2image** - PDF to image conversion for OCR

### Frontend
- **Vanilla JavaScript** - Modern ES6+ features
- **HTML5/CSS3** - Semantic markup and responsive design
- **Fetch API** - Asynchronous HTTP requests

### DevOps & Deployment
- **Docker** - Containerization for consistent deployments
- **Uvicorn** - ASGI server for production
- **CORS** - Cross-origin resource sharing configuration

### Prerequisites
- Python 3.9+
- Docker (optional)
- Tesseract OCR
- Poppler utilities

