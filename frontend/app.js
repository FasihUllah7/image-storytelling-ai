/**
 * Frontend application for Multimodal Image Understanding & Storytelling AI
 */

// Configuration - Use environment variable or fallback to localhost
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:5000/api'
    : 'https://your-backend-name.vercel.app/api'; // Update this after deploying backend

// State
let selectedImage = null;
let cameraStream = null;

// DOM Elements
const elements = {
    // Tabs
    tabBtns: document.querySelectorAll('.tab-btn'),
    tabContents: document.querySelectorAll('.tab-content'),

    // Upload
    dropzone: document.getElementById('dropzone'),
    fileInput: document.getElementById('file-input'),
    browseBtn: document.getElementById('browse-btn'),

    // Camera
    cameraVideo: document.getElementById('camera-video'),
    cameraCanvas: document.getElementById('camera-canvas'),
    startCameraBtn: document.getElementById('start-camera-btn'),
    captureBtn: document.getElementById('capture-btn'),
    stopCameraBtn: document.getElementById('stop-camera-btn'),

    // Preview
    imagePreview: document.getElementById('image-preview'),
    previewImg: document.getElementById('preview-img'),
    clearImageBtn: document.getElementById('clear-image-btn'),
    analyzeBtn: document.getElementById('analyze-btn'),

    // States
    loadingState: document.getElementById('loading-state'),
    resultsSection: document.getElementById('results-section'),
    errorState: document.getElementById('error-state'),
    errorMessage: document.getElementById('error-message'),

    // Results
    resultCaption: document.getElementById('result-caption'),
    resultSummary: document.getElementById('result-summary'),
    resultObjects: document.getElementById('result-objects'),
    resultMood: document.getElementById('result-mood'),
    resultStory: document.getElementById('result-story'),

    // Actions
    newAnalysisBtn: document.getElementById('new-analysis-btn'),
    retryBtn: document.getElementById('retry-btn'),

    // Theme
    themeToggle: document.getElementById('theme-toggle')
};

// ===== Theme Toggle =====
function initTheme() {
    // Check for saved theme preference or default to 'dark'
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

elements.themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// Initialize theme on load
initTheme();

// ===== Tab Switching =====
elements.tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Update active states
        elements.tabBtns.forEach(b => b.classList.remove('active'));
        elements.tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(`${tabName}-tab`).classList.add('active');

        // Stop camera if switching away
        if (tabName !== 'camera' && cameraStream) {
            stopCamera();
        }
    });
});

// ===== File Upload =====
elements.browseBtn.addEventListener('click', () => {
    elements.fileInput.click();
});

elements.fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleImageFile(file);
    }
});

// Drag and drop
elements.dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    elements.dropzone.classList.add('drag-over');
});

elements.dropzone.addEventListener('dragleave', () => {
    elements.dropzone.classList.remove('drag-over');
});

elements.dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    elements.dropzone.classList.remove('drag-over');

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleImageFile(file);
    } else {
        showError('Please drop a valid image file');
    }
});

elements.dropzone.addEventListener('click', () => {
    elements.fileInput.click();
});

// ===== Camera Capture =====
elements.startCameraBtn.addEventListener('click', async () => {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' }
        });

        elements.cameraVideo.srcObject = cameraStream;
        elements.cameraVideo.hidden = false;
        elements.startCameraBtn.hidden = true;
        elements.captureBtn.hidden = false;
        elements.stopCameraBtn.hidden = false;
    } catch (error) {
        showError('Failed to access camera: ' + error.message);
    }
});

elements.captureBtn.addEventListener('click', () => {
    const canvas = elements.cameraCanvas;
    const video = elements.cameraVideo;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    canvas.toBlob((blob) => {
        handleImageFile(blob);
        stopCamera();
    }, 'image/jpeg', 0.95);
});

elements.stopCameraBtn.addEventListener('click', () => {
    stopCamera();
});

function stopCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    elements.cameraVideo.srcObject = null;
    elements.cameraVideo.hidden = true;
    elements.startCameraBtn.hidden = false;
    elements.captureBtn.hidden = true;
    elements.stopCameraBtn.hidden = true;
}

// ===== Image Handling =====
function handleImageFile(file) {
    selectedImage = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        elements.previewImg.src = e.target.result;
        elements.imagePreview.hidden = false;

        // Hide other states
        elements.resultsSection.hidden = true;
        elements.errorState.hidden = true;
    };
    reader.readAsDataURL(file);
}

elements.clearImageBtn.addEventListener('click', () => {
    clearImage();
});

function clearImage() {
    selectedImage = null;
    elements.imagePreview.hidden = true;
    elements.previewImg.src = '';
    elements.fileInput.value = '';
}

// ===== Analysis =====
elements.analyzeBtn.addEventListener('click', async () => {
    if (!selectedImage) {
        showError('Please select an image first');
        return;
    }

    // Show loading state
    elements.imagePreview.hidden = true;
    elements.loadingState.hidden = false;
    elements.resultsSection.hidden = true;
    elements.errorState.hidden = true;

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('image', selectedImage);

        // Call API
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Analysis failed');
        }

        // Display results
        displayResults(data.results);

    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message);
    } finally {
        elements.loadingState.hidden = true;
    }
});

function displayResults(results) {
    // Display hero image (same as preview image)
    const analyzedImage = document.getElementById('analyzed-image');
    analyzedImage.src = elements.previewImg.src;

    // Populate caption overlay on hero image
    elements.resultCaption.textContent = results.caption || 'N/A';

    // Populate primary summary
    elements.resultSummary.textContent = results.summary || 'N/A';

    // Populate mood
    elements.resultMood.textContent = results.mood || 'N/A';

    // Populate story
    elements.resultStory.textContent = results.story || 'N/A';

    // Handle objects list (may be bulleted)
    if (results.objects) {
        // If already formatted with bullets, use as-is
        if (results.objects.includes('-') || results.objects.includes('•')) {
            elements.resultObjects.innerHTML = results.objects
                .split('\n')
                .filter(line => line.trim())
                .map(line => `<div>${line}</div>`)
                .join('');
        } else {
            // Otherwise, format as list
            elements.resultObjects.textContent = results.objects;
        }
    } else {
        elements.resultObjects.textContent = 'N/A';
    }

    // Show results section
    elements.resultsSection.hidden = false;

    // Scroll to results
    elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===== Error Handling =====
function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorState.hidden = false;
    elements.loadingState.hidden = true;
    elements.resultsSection.hidden = true;
}

elements.retryBtn.addEventListener('click', () => {
    elements.errorState.hidden = true;
    elements.imagePreview.hidden = false;
});

// ===== New Analysis =====
elements.newAnalysisBtn.addEventListener('click', () => {
    clearImage();
    elements.resultsSection.hidden = true;

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// ===== Health Check on Load =====
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        console.log('Backend status:', data);
    } catch (error) {
        console.warn('Backend not available:', error.message);
        console.log('Make sure to start the backend server: python backend/app.py');
    }
});
