// Surveillance System JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the surveillance system
    initializeSurveillanceSystem();
    
    // Auto-refresh functionality
    setInterval(updateDashboard, 30000); // Update every 30 seconds
    
    // Initialize tooltips
    initializeTooltips();
    
    // Real-time clock
    updateClock();
    setInterval(updateClock, 1000);
});

function initializeSurveillanceSystem() {
    console.log('Surveillance System Initialized');
    
    // Mock video stream initialization
    initializeMockVideoStreams();
    
    // Initialize alert system
    initializeAlertSystem();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
}

function initializeMockVideoStreams() {
    const videoPlaceholders = document.querySelectorAll('.video-placeholder');
    
    videoPlaceholders.forEach(placeholder => {
        // Add subtle animation to indicate "live" feed
        placeholder.style.position = 'relative';
        
        // Add mock streaming indicator
        const streamIndicator = document.createElement('div');
        streamIndicator.innerHTML = '<i data-feather="circle" style="width: 8px; height: 8px; color: #10B981;"></i> LIVE';
        streamIndicator.style.position = 'absolute';
        streamIndicator.style.top = '8px';
        streamIndicator.style.left = '8px';
        streamIndicator.style.background = 'rgba(0, 0, 0, 0.7)';
        streamIndicator.style.color = 'white';
        streamIndicator.style.padding = '2px 6px';
        streamIndicator.style.borderRadius = '4px';
        streamIndicator.style.fontSize = '10px';
        streamIndicator.style.fontWeight = 'bold';
        streamIndicator.style.display = 'flex';
        streamIndicator.style.alignItems = 'center';
        streamIndicator.style.gap = '4px';
        
        placeholder.appendChild(streamIndicator);
        
        // Refresh feather icons
        feather.replace();
    });
}

function initializeAlertSystem() {
    // Mock real-time alerts
    const alertTypes = ['motion', 'object', 'boundary', 'loitering'];
    const severities = ['low', 'medium', 'high', 'critical'];
    
    // Simulate new alerts every 2-5 minutes
    setInterval(() => {
        if (Math.random() < 0.3) { // 30% chance of new alert
            const mockAlert = {
                type: alertTypes[Math.floor(Math.random() * alertTypes.length)],
                severity: severities[Math.floor(Math.random() * severities.length)],
                camera: `Camera ${Math.floor(Math.random() * 6) + 1}`,
                timestamp: new Date().toLocaleTimeString()
            };
            
            showNewAlertNotification(mockAlert);
        }
    }, Math.random() * 180000 + 120000); // 2-5 minutes
}

function showNewAlertNotification(alert) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = 'toast position-fixed bottom-0 end-0 m-3';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header">
            <i data-feather="alert-triangle" class="me-2" style="width: 16px; height: 16px; color: #EF4444;"></i>
            <strong class="me-auto">New Alert</strong>
            <small>${alert.timestamp}</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">
            <strong>${alert.severity.toUpperCase()}</strong> ${alert.type} detected at ${alert.camera}
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Refresh feather icons
    feather.replace();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        document.body.removeChild(toast);
    });
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + D: Dashboard
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            window.location.href = '/dashboard';
        }
        
        // Ctrl/Cmd + C: Cameras
        if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
            e.preventDefault();
            window.location.href = '/cameras';
        }
        
        // Ctrl/Cmd + A: Alerts
        if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
            e.preventDefault();
            window.location.href = '/alerts';
        }
        
        // Ctrl/Cmd + F: Forensic Search
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            e.preventDefault();
            if (document.querySelector('[href="/forensic"]')) {
                window.location.href = '/forensic';
            }
        }
    });
}

function updateDashboard() {
    // Update timestamps
    const timeElements = document.querySelectorAll('.alert-time');
    timeElements.forEach(element => {
        if (element.textContent.includes(':')) {
            // This is a time element, could be updated with real-time data
            console.log('Updating dashboard element:', element);
        }
    });
    
    // Update camera status indicators
    updateCameraStatuses();
}

function updateCameraStatuses() {
    const statusElements = document.querySelectorAll('.camera-status');
    statusElements.forEach(element => {
        // Simulate random status changes (very rarely)
        if (Math.random() < 0.01) { // 1% chance
            const statuses = ['online', 'offline', 'maintenance'];
            const currentStatus = Array.from(element.classList).find(cls => cls.startsWith('status-'));
            const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
            
            if (currentStatus) {
                element.classList.remove(currentStatus);
            }
            element.classList.add(`status-${newStatus}`);
            element.querySelector('.status-icon').nextSibling.textContent = newStatus.charAt(0).toUpperCase() + newStatus.slice(1);
        }
    });
}

function updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    
    // Update any clock elements
    const clockElements = document.querySelectorAll('.system-clock');
    clockElements.forEach(element => {
        element.textContent = timeString;
    });
}

// Camera control functions
function playCamera(cameraId) {
    console.log(`Playing camera ${cameraId}`);
    // Mock camera play functionality
    showNotification('Camera playback started', 'info');
}

function pauseCamera(cameraId) {
    console.log(`Pausing camera ${cameraId}`);
    // Mock camera pause functionality
    showNotification('Camera playback paused', 'info');
}

function maximizeCamera(cameraId) {
    console.log(`Maximizing camera ${cameraId}`);
    // Mock camera maximize functionality
    showNotification('Camera maximized', 'info');
}

// Utility functions
function showNotification(message, type = 'info') {
    const colors = {
        info: '#3B82F6',
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444'
    };
    
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type]};
        color: white;
        padding: 12px 16px;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1050;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove notification after 3 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

function exportData(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Chart utilities
function createChart(ctx, config) {
    return new Chart(ctx, config);
}

// Search and filter utilities
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Mock data generators for testing
function generateMockEvent() {
    const eventTypes = ['person', 'vehicle', 'object', 'motion'];
    const cameras = ['Camera 1', 'Camera 2', 'Camera 3', 'Camera 4', 'Camera 5', 'Camera 6'];
    
    return {
        id: Math.floor(Math.random() * 10000),
        timestamp: new Date(),
        camera: cameras[Math.floor(Math.random() * cameras.length)],
        type: eventTypes[Math.floor(Math.random() * eventTypes.length)],
        confidence: Math.random() * 0.4 + 0.6 // 60-100%
    };
}

// Export for global use
window.SurveillanceSystem = {
    playCamera,
    pauseCamera,
    maximizeCamera,
    showNotification,
    formatTimestamp,
    exportData,
    generateMockEvent
};
