/**
 * PortScanPy Web Interface
 * Frontend JavaScript for handling scan requests and displaying results
 */

// DOM elements
const scanForm = document.getElementById('scanForm');
const scanBtn = document.getElementById('scanBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsDiv = document.getElementById('results');
const resultMeta = document.getElementById('resultMeta');

// Event listeners
scanForm.addEventListener('submit', handleScanSubmit);
clearBtn.addEventListener('click', clearResults);

/**
 * Handle scan form submission
 */
async function handleScanSubmit(e) {
    e.preventDefault();

    // Get form values
    const formData = {
        target: document.getElementById('target').value.trim(),
        ports: document.getElementById('ports').value.trim(),
        timeout: parseFloat(document.getElementById('timeout').value),
        workers: parseInt(document.getElementById('workers').value)
    };

    // Validate
    if (!formData.target) {
        showError('Please enter a target hostname or IP address');
        return;
    }

    // Disable form
    setFormEnabled(false);

    // Show loading state
    showLoading();

    try {
        // Make API request
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred during scanning');
        }
    } catch (error) {
        showError(`Network error: ${error.message}`);
    } finally {
        setFormEnabled(true);
    }
}

/**
 * Display scan results in terminal-like output
 */
function displayResults(data) {
    const { target, ports_scanned, results, total_ports, open_ports, scan_time_seconds } = data;

    // Update meta info
    resultMeta.textContent = `${open_ports} open / ${total_ports} total`;

    // Build output HTML
    let html = `
        <div class="scan-header">
            PortScanPy - scan results for ${escapeHtml(target)}
        </div>

        <div class="scan-info">
            Ports: ${escapeHtml(ports_scanned)} | Scan time: ${scan_time_seconds}s
        </div>
    `;

    if (results.length === 0) {
        html += `
            <div class="scan-info">
                No open ports found.
            </div>
        `;
    } else {
        results.forEach(result => {
            const service = result.service || 'unknown';
            html += `
                <div class="result-line">
                    <span class="result-icon">[+]</span>
                    <span class="result-port">${result.port}/tcp</span>
                    <span class="result-status">${result.status}</span>
                    <span class="result-service">${escapeHtml(service)}</span>
                </div>
            `;
        });
    }

    html += `
        <div class="scan-summary">
            <div class="scan-summary-line">
                Scan complete in <span class="highlight">${scan_time_seconds}</span> seconds.
            </div>
            <div class="scan-summary-line">
                Open ports: <span class="highlight">${open_ports}</span>
            </div>
        </div>
    `;

    resultsDiv.innerHTML = html;
}

/**
 * Show loading state
 */
function showLoading() {
    resultMeta.textContent = 'Scanning...';
    resultsDiv.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <span>Scanning ports...</span>
        </div>
    `;
}

/**
 * Show error message
 */
function showError(message) {
    resultMeta.textContent = 'Error';
    resultsDiv.innerHTML = `
        <div class="error-message">
            <svg class="error-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <div>
                <strong>Error:</strong> ${escapeHtml(message)}
            </div>
        </div>
    `;
}

/**
 * Clear results
 */
function clearResults() {
    resultMeta.textContent = '';
    resultsDiv.innerHTML = `
        <div class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
            </svg>
            <p>No scan results yet</p>
            <p class="hint">Enter a target and press "Run Scan" to begin</p>
        </div>
    `;
}

/**
 * Enable/disable form
 */
function setFormEnabled(enabled) {
    scanBtn.disabled = !enabled;
    document.getElementById('target').disabled = !enabled;
    document.getElementById('ports').disabled = !enabled;
    document.getElementById('timeout').disabled = !enabled;
    document.getElementById('workers').disabled = !enabled;

    if (enabled) {
        scanBtn.innerHTML = '<span class="btn-icon">▶</span> Run Scan';
    } else {
        scanBtn.innerHTML = '<span class="btn-icon">⏸</span> Scanning...';
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Update status indicator based on API health
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();

        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-indicator span:last-child');

        if (data.status === 'ok') {
            statusDot.style.background = '#4ec9b0';
            statusText.textContent = 'Ready';
        }
    } catch (error) {
        const statusDot = document.querySelector('.status-dot');
        const statusText = document.querySelector('.status-indicator span:last-child');
        statusDot.style.background = '#f48771';
        statusText.textContent = 'Disconnected';
    }
}

// Check health on load and periodically
checkHealth();
setInterval(checkHealth, 30000); // Check every 30 seconds
