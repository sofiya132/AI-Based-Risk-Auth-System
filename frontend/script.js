// ─── API Base URL ─────────────────────────────────────────────────────────────
const API_BASE = "https://ai-based-risk-auth-system.onrender.com/api";

// Warm up the backend immediately on any page load
// This wakes the free Render instance so it's ready by the time user submits
fetch("https://ai-based-risk-auth-system.onrender.com/").catch(() => {});


// ─── Token Helpers ────────────────────────────────────────────────────────────

function saveToken(token) {
    localStorage.setItem("auth_token", token);
}

function getToken() {
    return localStorage.getItem("auth_token");
}

function clearToken() {
    localStorage.removeItem("auth_token");
}


// ─── Auth Guard ───────────────────────────────────────────────────────────────

function redirectIfLoggedIn() {
    if (getToken()) {
        window.location.href = "dashboard.html";
    }
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

// Alias used by dashboard.html
function requireLogin() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

function removeToken() {
    localStorage.removeItem("auth_token");
}

// Authenticated API request — automatically adds Bearer token header
async function apiRequest(path, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + getToken()
        }
    };
    if (body) options.body = JSON.stringify(body);
    return fetch(`${API_BASE}${path}`, options);
}


// ─── Device Fingerprint ───────────────────────────────────────────────────────

function getDeviceFingerprint() {
    const nav = window.navigator;
    const raw = [
        nav.userAgent,
        nav.language,
        screen.width + "x" + screen.height,
        new Date().getTimezoneOffset()
    ].join("|");

    // Simple hash
    let hash = 0;
    for (let i = 0; i < raw.length; i++) {
        hash = (hash << 5) - hash + raw.charCodeAt(i);
        hash |= 0;
    }
    return "fp_" + Math.abs(hash).toString(16);
}


// ─── UI Helpers ───────────────────────────────────────────────────────────────

function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = "alert " + type;
    el.style.display = "block";
}

function hideAlert(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.style.display = "none";
}

function setButtonLoading(btn, isLoading, originalText) {
    if (isLoading) {
        btn.disabled = true;
        btn.textContent = "Please wait...";
    } else {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}