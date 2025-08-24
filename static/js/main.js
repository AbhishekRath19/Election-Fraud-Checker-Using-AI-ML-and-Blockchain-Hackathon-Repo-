// Main JavaScript file for the voting system

// Function to display a confirmation dialog before submitting votes
function confirmVoteSubmission() {
    return confirm("Are you sure you want to submit your vote? This action cannot be undone.");
}

// Function to validate file uploads
function validateFileUpload(fileInput) {
    const file = fileInput.files[0];
    
    if (file) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        const maxSize = 5 * 1024 * 1024; // 5MB
        
        if (!allowedTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPEG, PNG, GIF)');
            return false;
        }
        
        if (file.size > maxSize) {
            alert('File size exceeds 5MB limit. Please upload a smaller file.');
            return false;
        }
    }
    
    return true;
}

// Function to handle form submissions
function handleFormSubmission(formId, submitCallback) {
    const form = document.getElementById(formId);
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (submitCallback) {
                if (!submitCallback()) {
                    e.preventDefault();
                }
            }
        });
    }
}

// Initialize form validation
document.addEventListener('DOMContentLoaded', function() {
    // Registration form validation
    const registrationForm = document.getElementById('registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('id_image');
            if (fileInput && !validateFileUpload(fileInput)) {
                e.preventDefault();
            }
        });
    }
    
    // Vote form confirmation
    const voteForm = document.getElementById('voteForm');
    if (voteForm) {
        voteForm.addEventListener('submit', function(e) {
            if (!confirmVoteSubmission()) {
                e.preventDefault();
            }
        });
    }
});

// Function to show/hide loading indicators
function showLoadingIndicator() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
}

function hideLoadingIndicator() {
    const loadingElement = document.getElementById('loading');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
}

// Function to display flash messages
function displayFlashMessage(message, type = 'info') {
    const flashContainer = document.querySelector('.flash-messages');
    
    if (flashContainer) {
        const messageElement = document.createElement('div');
        messageElement.className = `flash-message ${type}`;
        messageElement.textContent = message;
        
        flashContainer.appendChild(messageElement);
        
        // Auto-remove message after 5 seconds
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.parentNode.removeChild(messageElement);
            }
        }, 5000);
    }
}

// Export functions for global use
window.voteSystem = {
    confirmVoteSubmission,
    validateFileUpload,
    handleFormSubmission,
    showLoadingIndicator,
    hideLoadingIndicator,
    displayFlashMessage
};