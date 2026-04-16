// script.js — Shared JavaScript utilities for all pages

// ── Configuration ──────────────────────────────────────────────────────────
// Change this to your Render backend URL when deployed
const API_BASE = "https://ai-based-risk-auth-system.onrender.com";
// ── Device Fingerprinting ───────────────────────────────────────────────────
/**
 * Generate a simple device fingerprint from browser properties.
 * In production, use FingerprintJS library for better accuracy.
 * This creates a unique-ish string for this browser/device combo.
 */
function getDeviceFingerprint() {
    const components = [
        navigator.userAgent,           // Browser type and version
        navigator.language,            // Browser language (en-US, etc.)
        screen.width + "x" + screen.height,  // Screen resolution
        Intl.DateTimeFormat().resolvedOptions().timeZone,  // Timezone
        navigator.platform,            // OS platform
        navigator.hardwareConcurrency  // Number of CPU cores
    ];

    // Create a simple hash: sum up char codes of the joined string
    const str = components.join("|");
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;  // Bitwise hash
        hash = hash & hash;  // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(16);  // Return as hex string
}

// ── Alert Helper ───────────────────────────────────────────────────────────
/**
 * Show an alert message on the page.
 * @param {string} elementId - The ID of the .alert div
 * @param {string} message - Text to display
 * @param {string} type - "error" or "success"
 */
function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = `alert ${type}`;
    el.style.display = "block";
    // Auto-hide after 5 seconds
    setTimeout(() => { el.style.display = "none"; }, 5000);
}

// ── Token Storage ──────────────────────────────────────────────────────────
// Store/retrieve JWT token from localStorage
function saveToken(token) {
    localStorage.setItem("auth_token", token);
}

function getToken() {
    return localStorage.getItem("auth_token");
}

function removeToken() {
    localStorage.removeItem("auth_token");
}

// ── Auth Guard ────────────────────────────────────────────────────────────
/**
 * Redirect to login if no token found.
 * Call this at the top of protected pages like dashboard.html.
 */
function requireLogin() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

/**
 * Redirect to dashboard if already logged in.
 * Call this on login/register pages to prevent re-login.
 */
function redirectIfLoggedIn() {
    if (getToken()) {
        window.location.href = "dashboard.html";
    }
}

// ── API Request Helper ─────────────────────────────────────────────────────
/**
 * Make an authenticated API request (includes JWT in header).
 * @param {string} endpoint - API path like "/dashboard"
 * @param {string} method - "GET", "POST", etc.
 * @param {Object} body - Request body (for POST)
 */
async function apiRequest(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
            // Include JWT token in every request to protected endpoints
            "Authorization": `Bearer ${getToken()}`
        }
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);
    return response;
}

// ── Button Loading State ──────────────────────────────────────────────────
function setButtonLoading(btn, loading, originalText) {
    if (loading) {
        btn.disabled = true;
        btn.innerHTML = `<span class="spinner"></span>Loading...`;
    } else {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}