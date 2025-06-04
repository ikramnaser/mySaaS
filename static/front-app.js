document.addEventListener('DOMContentLoaded', () => {
    // API endpoint - use relative path when deployed together
    const API_URL = '/api'; // Will be served from the same domain when using Docker
    
    // DOM elements
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const selectedFile = document.getElementById('selected-file');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const processBtn = document.getElementById('process-btn');
    const progressContainer = document.getElementById('progress-container');
    const progressBar = document.getElementById('progress');
    const resultsSection = document.getElementById('results-section');
    const newUploadBtn = document.getElementById('new-upload-btn');
    const docType = document.getElementById('doc-type');
    const docConfidence = document.getElementById('doc-confidence');
    const entitiesResult = document.getElementById('entities-result');
    const extractedText = document.getElementById('extracted-text');
    const errorToast = document.getElementById('error-toast');
    const errorMessage = document.getElementById('error-message');
    const closeError = document.getElementById('close-error');
    
    let currentFile = null;
    
    // Event listeners
    uploadBtn.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    processBtn.addEventListener('click', processDocument);
    
    newUploadBtn.addEventListener('click', resetUI);
    
    closeError.addEventListener('click', () => {
        errorToast.classList.remove('show');
    });
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });
    
    // Handle file selection
    function handleFileSelection(file) {
        const allowedTypes = ['application/pdf', 'image/png', 'image/jpeg'];
        
        if (!allowedTypes.includes(file.type)) {
            showError('Invalid file type. Please upload a PDF, PNG, or JPG file.');
            return;
        }
        
        currentFile = file;
        
        // Update UI
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        
        uploadArea.hidden = true;
        selectedFile.hidden = false;
    }
    
    // Process document
    async function processDocument() {
        if (!currentFile) {
            showError('Please select a file first.');
            return;
        }
        
        // Show progress
        selectedFile.hidden = true;
        progressContainer.hidden = false;
        updateProgress(15); // Initial progress
        
        // Create form data
        const formData = new FormData();
        formData.append('file', currentFile);
        
        try {
            // Simulate progress
            let progress = 15;
            const progressInterval = setInterval(() => {
                progress += Math.random() * 10;
                if (progress > 90) {
                    progress = 90;
                    clearInterval(progressInterval);
                }
                updateProgress(progress);
            }, 500);
            
            // Send request
            const response = await fetch(`${API_URL}/upload`, {
                method: 'POST',
                body: formData
            });
            
            clearInterval(progressInterval);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to process document');
            }
            
            updateProgress(100);
            
            // Get results
            const result = await response.json();
            displayResults(result);
            
        } catch (error) {
            console.error('Error processing document:', error);
            showError(error.message || 'Failed to process document. Please try again.');
            resetUI();
        }
    }
    
    // Display results
    function displayResults(result) {
        // Update classification
        docType.textContent = capitalizeFirstLetter(result.classification.label);
        docConfidence.textContent = `${Math.round(result.classification.confidence * 100)}%`;
        
        // Update entities
        if (Object.keys(result.entities).length === 0) {
            entitiesResult.innerHTML = '<p class="loading-entities">No entities found</p>';
        } else {
            entitiesResult.innerHTML = '';
            
            for (const [entityType, entities] of Object.entries(result.entities)) {
                const entityGroup = document.createElement('div');
                entityGroup.className = 'entity-group';
                
                const entityTypeEl = document.createElement('p');
                entityTypeEl.className = 'entity-type';
                entityTypeEl.textContent = formatEntityType(entityType);
                entityGroup.appendChild(entityTypeEl);
                
                entities.forEach(entity => {
                    const entityItem = document.createElement('div');
                    entityItem.className = 'entity-item';
                    entityItem.textContent = entity.text;
                    entityGroup.appendChild(entityItem);
                });
                
                entitiesResult.appendChild(entityGroup);
            }
        }
        
        // Update extracted text
        extractedText.textContent = result.text || 'No text extracted';
        
        // Show results
        progressContainer.hidden = true;
        resultsSection.hidden = false;
    }
    
    // Helper functions
    function updateProgress(value) {
        progressBar.style.width = `${value}%`;
    }
    
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    function resetUI() {
        // Reset file
        currentFile = null;
        fileInput.value = '';
        
        // Reset UI elements
        uploadArea.hidden = false;
        selectedFile.hidden = true;
        progressContainer.hidden = true;
        resultsSection.hidden = true;
        updateProgress(0);
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorToast.classList.add('show');
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            errorToast.classList.remove('show');
        }, 5000);
    }
    
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    function formatEntityType(type) {
        // Format entity types from spaCy
        const entityMap = {
            'PER': 'Person',
            'ORG': 'Organization',
            'LOC': 'Location',
            'GPE': 'Geopolitical Entity',
            'DATE': 'Date',
            'TIME': 'Time',
            'MONEY': 'Money',
            'PERCENT': 'Percentage',
            'PRODUCT': 'Product',
            'EVENT': 'Event',
            'WORK_OF_ART': 'Work of Art',
            'LAW': 'Law',
            'LANGUAGE': 'Language'
        };
        
        return entityMap[type] || type;
    }
});