// RMGFraud - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation
    initializeFormValidation();
    
    // Search functionality
    initializeSearch();
    
    // Risk level indicators
    initializeRiskIndicators();
    
    // Security features
    initializeSecurityFeatures();
});

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('q');
    if (searchInput) {
        // Debounce search
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(this.value);
            }, 300);
        });
    }
}

// Perform search with AJAX
function performSearch(query) {
    if (query.length < 2) return;
    
    fetch(`/database/search?q=${encodeURIComponent(query)}`, {
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        displaySearchResults(data);
    })
    .catch(error => {
        console.error('Search error:', error);
    });
}

// Display search results
function displaySearchResults(results) {
    const resultsContainer = document.getElementById('searchResults');
    if (!resultsContainer) return;
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="text-center text-muted">No results found</div>';
        return;
    }
    
    const html = results.map(entity => `
        <div class="search-result-item p-3 border-bottom">
            <div class="d-flex justify-content-between align-items-start">
                <div>
                    <h6 class="mb-1">${entity.name}</h6>
                    <small class="text-muted">${entity.entity_type} • ${entity.country_code}</small>
                </div>
                <span class="badge bg-${getRiskBadgeColor(entity.risk_level)}">${entity.risk_level}</span>
            </div>
        </div>
    `).join('');
    
    resultsContainer.innerHTML = html;
}

// Risk level indicators
function initializeRiskIndicators() {
    const riskElements = document.querySelectorAll('[data-risk-level]');
    
    riskElements.forEach(element => {
        const riskLevel = element.getAttribute('data-risk-level');
        element.classList.add(`risk-${riskLevel.toLowerCase()}`);
        
        // Add appropriate icon
        const icon = element.querySelector('.risk-icon');
        if (icon) {
            icon.className = `risk-icon fas ${getRiskIcon(riskLevel)}`;
        }
    });
}

// Get risk badge color
function getRiskBadgeColor(riskLevel) {
    const colors = {
        'Low': 'success',
        'Medium': 'warning',
        'High': 'danger',
        'Critical': 'dark'
    };
    return colors[riskLevel] || 'secondary';
}

// Get risk icon
function getRiskIcon(riskLevel) {
    const icons = {
        'Low': 'fa-check-circle',
        'Medium': 'fa-exclamation-triangle',
        'High': 'fa-exclamation-circle',
        'Critical': 'fa-times-circle'
    };
    return icons[riskLevel] || 'fa-question-circle';
}

// Security features
function initializeSecurityFeatures() {
    // Auto-logout warning
    let inactivityTimer;
    const warningTime = 10 * 60 * 1000; // 10 minutes
    const logoutTime = 15 * 60 * 1000; // 15 minutes
    
    function resetTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(showLogoutWarning, warningTime);
    }
    
    function showLogoutWarning() {
        if (confirm('You will be logged out due to inactivity. Click OK to stay logged in.')) {
            resetTimer();
        } else {
            setTimeout(logout, logoutTime - warningTime);
        }
    }
    
    function logout() {
        window.location.href = '/auth/logout';
    }
    
    // Reset timer on user activity
    ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'].forEach(event => {
        document.addEventListener(event, resetTimer, true);
    });
    
    resetTimer();
    
    // Secure form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add CSRF token if not present
            if (!form.querySelector('input[name="csrf_token"]')) {
                const csrfToken = document.querySelector('meta[name="csrf-token"]');
                if (csrfToken) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.name = 'csrf_token';
                    input.value = csrfToken.getAttribute('content');
                    form.appendChild(input);
                }
            }
        });
    });
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for global use
window.RMGFraud = {
    formatDate,
    formatDateTime,
    getRiskBadgeColor,
    getRiskIcon
};
