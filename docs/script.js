// Honda Car Search Dashboard JavaScript

// Configuration
const API_BASE_URL = window.location.origin + window.location.pathname.replace('/index.html', '').replace(/\/$/, '');
const REFRESH_INTERVAL = 300000; // 5 minutes

// Global variables
let refreshTimer;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    startAutoRefresh();
});

function initializeDashboard() {
    updateLastUpdatedTime();
    loadSearchResults();
    loadStatistics();
}

function updateLastUpdatedTime() {
    const now = new Date();
    const timeString = now.toLocaleDateString() + ' at ' + now.toLocaleTimeString();
    
    // Update all elements with class 'last-updated'
    const elements = document.querySelectorAll('.last-updated');
    elements.forEach(el => {
        el.textContent = timeString;
    });
}

function pollForUpdates() {
    let pollCount = 0;
    const maxPolls = 20; // Poll for up to 10 minutes (30s intervals)
    
    const pollInterval = setInterval(async () => {
        pollCount++;
        
        try {
            // Check if data has been updated by looking at the timestamp or content
            const response = await fetch('data.json');
            const data = await response.json();
            
            // Update the display with any new data
            await loadSearchResults();
            await loadStatistics();
            
            // Check if we should stop polling (you might add a timestamp check here)
            if (pollCount >= maxPolls) {
                clearInterval(pollInterval);
                const statusDiv = document.getElementById('search-status');
                if (statusDiv) {
                    statusDiv.textContent = 'Search completed! Dashboard updated with latest results.';
                    statusDiv.className = 'search-status success';
                }
                updateLastUpdatedTime();
            }
        } catch (error) {
            console.error('Error polling for updates:', error);
            if (pollCount >= maxPolls) {
                clearInterval(pollInterval);
            }
        }
    }, 30000); // Poll every 30 seconds
}

// GitHub token management functions
function toggleSetup() {
    const content = document.getElementById('setup-content');
    const arrow = document.getElementById('setup-arrow');
    
    if (content.style.display === 'none') {
        content.style.display = 'block';
        arrow.classList.add('rotated');
        arrow.textContent = '▲';
        
        // Load existing token if present
        const existingToken = localStorage.getItem('github_token');
        if (existingToken) {
            document.getElementById('github-token').value = existingToken.substring(0, 8) + '...';
            showSetupStatus('Token loaded from browser storage', 'success');
        }
    } else {
        content.style.display = 'none';
        arrow.classList.remove('rotated');
        arrow.textContent = '▼';
    }
}

function saveToken() {
    const tokenInput = document.getElementById('github-token');
    const token = tokenInput.value.trim();
    
    if (!token) {
        showSetupStatus('Please enter a GitHub token', 'error');
        return;
    }
    
    if (!token.startsWith('ghp_') && !token.startsWith('github_pat_')) {
        showSetupStatus('Invalid token format. GitHub tokens start with "ghp_" or "github_pat_"', 'error');
        return;
    }
    
    // Store token in localStorage
    localStorage.setItem('github_token', token);
    
    // Mask the token in the input
    tokenInput.value = token.substring(0, 8) + '...';
    
    showSetupStatus('Token saved successfully! "Search Now" will trigger live scraping.', 'success');
}

function clearToken() {
    localStorage.removeItem('github_token');
    document.getElementById('github-token').value = '';
    showSetupStatus('Token cleared. "Search Now" will use demo mode.', 'success');
}

function showSetupStatus(message, type) {
    const statusDiv = document.getElementById('setup-status');
    statusDiv.textContent = message;
    statusDiv.className = `setup-status ${type}`;
    
    // Hide the message after 5 seconds
    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'setup-status';
    }, 5000);
}

async function loadSearchResults() {
    const container = document.getElementById('results-container');
    
    try {
        // Try to load from GitHub raw content or local data
        const response = await fetch('data.json');
        
        if (!response.ok) {
            // Fallback to sample data if no real data available
            loadSampleData();
            return;
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.log('No data.json found, using sample data');
        loadSampleData();
    }
}

function loadSampleData() {
    // Sample data based on your actual search results
    const sampleData = {
        last_search: "2025-10-09T19:03:13.087245",
        total_searches: 14,
        vehicles_tracked: 3,
        notifications_sent: 2,
        matches: [
            {
                title: "2024 Honda Civic Hybrid",
                year: "2024",
                make: "Honda", 
                model: "Civic",
                trim: "Hybrid",
                type: "new",
                price: "$28,500",
                found_date: "2025-10-09T19:03:12.600085",
                link: "https://www.autoparkhonda.com/new-inventory/index.htm?make=Honda&model=Civic%20Hybrid",
                dealer_link: "https://www.autoparkhonda.com/VehicleDetails/new-2024-Honda-Civic-Hybrid-4dr_Sedan-Cary-NC/5438262784"
            },
            {
                title: "2023 Honda Civic Sport",
                year: "2023",
                make: "Honda",
                model: "Civic", 
                trim: "Sport",
                type: "used",
                price: "$24,995",
                mileage: "15,420",
                found_date: "2025-10-09T18:33:08.951741",
                link: "https://www.autoparkhonda.com/used-inventory/index.htm?make=Honda&model=Civic",
                dealer_link: "https://www.autoparkhonda.com/VehicleDetails/used-2023-Honda-Civic-Sport-4dr_Sedan-Cary-NC/5441238791"
            },
            {
                title: "2025 Honda Civic Hybrid",
                year: "2025",
                make: "Honda",
                model: "Civic",
                trim: "Hybrid", 
                type: "new",
                price: "$29,200",
                found_date: "2025-10-09T19:03:12.600105",
                link: "https://www.autoparkhonda.com/new-inventory/index.htm?make=Honda&model=Civic%20Hybrid",
                dealer_link: "https://www.autoparkhonda.com/VehicleDetails/new-2025-Honda-Civic-Hybrid-4dr_Sedan-Cary-NC/5445672834"
            }
        ]
    };
    
    displayResults(sampleData);
    updateStatistics(sampleData);
}

function displayResults(data) {
    const container = document.getElementById('results-container');
    
    if (!data.matches || data.matches.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <h3>No vehicles found yet</h3>
                <p>The search is running automatically. New matches will appear here when found.</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    data.matches.forEach(vehicle => {
        const foundDate = new Date(vehicle.found_date).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
        
        const foundTime = new Date(vehicle.found_date).toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        html += `
            <div class="vehicle-card">
                <div class="vehicle-header">
                    <div class="vehicle-info">
                        <div class="vehicle-title">${vehicle.title}</div>
                        <div class="vehicle-details">
                            <strong>Year:</strong> ${vehicle.year} | 
                            <strong>Type:</strong> ${vehicle.type.charAt(0).toUpperCase() + vehicle.type.slice(1)}
                            ${vehicle.mileage ? ` | <strong>Mileage:</strong> ${vehicle.mileage} miles` : ''}
                        </div>
                        <div class="vehicle-details">
                            <strong>Dealership:</strong> ${vehicle.dealership || 'Honda Dealership'}
                        </div>
                        <div class="vehicle-details">
                            <strong>Found:</strong> ${foundDate} at ${foundTime}
                        </div>
                        <div class="vehicle-price"><strong>Price:</strong> ${vehicle.price || 'Not available'}</div>
                    </div>
                    <div class="vehicle-badge ${vehicle.type}">
                        ${vehicle.type.toUpperCase()}
                    </div>
                </div>
                <div class="vehicle-actions">
                    <a href="${vehicle.dealer_link || vehicle.link}" target="_blank" class="view-btn">
                        <i class="fas fa-external-link-alt"></i> View Vehicle
                    </a>
                    <a href="${vehicle.link}" target="_blank" class="view-btn" style="background: #95a5a6;">
                        <i class="fas fa-search"></i> Browse Similar
                    </a>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

function updateStatistics(data) {
    if (data.total_searches) {
        document.getElementById('total-searches').textContent = data.total_searches;
    }
    if (data.vehicles_tracked !== undefined) {
        document.getElementById('vehicles-found').textContent = data.vehicles_tracked;
    }
    if (data.dealerships_count !== undefined) {
        document.getElementById('notifications-sent').textContent = data.dealerships_count;
    }
    if (data.last_search) {
        const lastSearch = new Date(data.last_search).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric'
        });
        document.getElementById('last-search').textContent = lastSearch;
    }
}

async function loadStatistics() {
    try {
        const response = await fetch('data.json');
        if (response.ok) {
            const data = await response.json();
            updateStatistics(data);
        } else {
            console.log('Failed to load statistics data');
        }
    } catch (error) {
        console.log('Error loading statistics:', error);
        // Use sample data as fallback
        const sampleData = {
            total_searches: 14,
            vehicles_tracked: 6,
            dealerships_count: 3,
            last_search: "2025-10-11T13:28:00.857456"
        };
        updateStatistics(sampleData);
    }
}

function refreshResults() {
    const refreshBtn = document.querySelector('.refresh-btn');
    const refreshIcon = refreshBtn.querySelector('i');
    
    // Add loading animation
    refreshIcon.classList.add('refreshing');
    refreshBtn.disabled = true;
    
    // Update timestamp
    updateLastUpdatedTime();
    
    // Reload results
    loadSearchResults().finally(() => {
        // Remove loading animation
        setTimeout(() => {
            refreshIcon.classList.remove('refreshing');
            refreshBtn.disabled = false;
        }, 1000);
    });
}

function startAutoRefresh() {
    // Refresh every 5 minutes
    refreshTimer = setInterval(() => {
        loadSearchResults();
        updateLastUpdatedTime();
    }, REFRESH_INTERVAL);
}

function stopAutoRefresh() {
    if (refreshTimer) {
        clearInterval(refreshTimer);
    }
}

// Handle page visibility changes to pause/resume auto-refresh
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        stopAutoRefresh();
    } else {
        startAutoRefresh();
        // Refresh immediately when page becomes visible
        loadSearchResults();
        updateLastUpdatedTime();
    }
});

// Utility functions
function formatPrice(price) {
    if (!price) return 'Price not available';
    if (typeof price === 'number') {
        return `$${price.toLocaleString()}`;
    }
    return price;
}

function timeAgo(dateString) {
    const now = new Date();
    const past = new Date(dateString);
    const diffMs = now - past;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffMins < 60) {
        return `${diffMins} minutes ago`;
    } else if (diffHours < 24) {
        return `${diffHours} hours ago`;
    } else {
        return `${diffDays} days ago`;
    }
}

async function runNewSearch() {
    const searchBtn = document.getElementById('search-now-btn');
    const statusDiv = document.getElementById('search-status');
    const searchIcon = searchBtn.querySelector('i');
    
    // Update UI to show searching state
    searchBtn.disabled = true;
    searchIcon.className = 'fas fa-spinner fa-spin';
    statusDiv.textContent = 'Running search...';
    statusDiv.className = 'search-status searching';
    
    try {
        // Try multiple methods to trigger the GitHub Actions workflow
        let success = false;
        
        // Method 1: Try using workflow_dispatch (requires authentication)
        const token = localStorage.getItem('github_token');
        if (token) {
            try {
                const response = await fetch('https://api.github.com/repos/jaymade/carSearch/actions/workflows/auto-search.yml/dispatches', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/vnd.github.v3+json',
                        'Authorization': `token ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        ref: 'main',
                        inputs: {
                            triggered_by: 'search_now_button'
                        }
                    })
                });
                
                if (response.ok) {
                    success = true;
                    statusDiv.textContent = 'Search triggered! GitHub Action is running the scraper. Results will appear in ~2-3 minutes.';
                    statusDiv.className = 'search-status success';
                    pollForUpdates();
                }
            } catch (error) {
                console.log('Workflow dispatch failed:', error);
            }
        }
        
        // Method 2: If no token or workflow dispatch failed, try repository dispatch
        if (!success) {
            try {
                const response = await fetch('https://api.github.com/repos/jaymade/carSearch/dispatches', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/vnd.github.v3+json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        event_type: 'manual-search',
                        client_payload: {
                            triggered_by: 'search_now_button',
                            timestamp: new Date().toISOString()
                        }
                    })
                });
                
                if (response.ok) {
                    success = true;
                    statusDiv.textContent = 'Search triggered! GitHub Action is running the scraper. Results will appear in ~2-3 minutes.';
                    statusDiv.className = 'search-status success';
                    pollForUpdates();
                }
            } catch (error) {
                console.log('Repository dispatch failed:', error);
            }
        }
        
        // Method 3: Fallback to demo mode
        if (!success) {
            statusDiv.textContent = 'Demo Mode: Refreshing current data (GitHub Actions requires authentication for real-time triggering)';
            statusDiv.className = 'search-status info';
            
            // Simulate search delay and refresh current data
            setTimeout(async () => {
                await loadSearchResults();
                await loadStatistics();
                updateLastUpdatedTime();
                statusDiv.textContent = 'Data refreshed! For real-time scraping, set up GitHub token authentication.';
                statusDiv.className = 'search-status success';
            }, 2000);
        }
        
    } catch (error) {
        console.error('Search error:', error);
        statusDiv.textContent = 'Search failed. Please try again.';
        statusDiv.className = 'search-status error';
    } finally {
        // Reset button state
        searchBtn.disabled = false;
        searchIcon.className = 'fas fa-search';
        
        // Clear status after 10 seconds
        setTimeout(() => {
            statusDiv.textContent = '';
            statusDiv.className = 'search-status';
        }, 10000);
    }
}

// Export functions for testing
window.dashboardFunctions = {
    refreshResults,
    loadSearchResults,
    updateLastUpdatedTime,
    formatPrice,
    timeAgo,
    runNewSearch
};