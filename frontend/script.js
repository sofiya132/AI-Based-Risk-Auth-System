// script.js — Shared JavaScript utilities for all pages

// ── Configuration ──────────────────────────────────────────────────────────
const API_BASE = "https://ai-based-risk-auth-system.onrender.com/api";

// ── Device Fingerprinting ───────────────────────────────────────────────────
/**
 * Generate a device fingerprint from browser properties.
 * Detects browser changes (Chrome vs Edge vs Firefox vs Safari)
 */
function getDeviceFingerprint() {
    const browserName =
        navigator.userAgent.includes("Edg/")     ? "edge" :
        navigator.userAgent.includes("Chrome")   ? "chrome" :
        navigator.userAgent.includes("Firefox")  ? "firefox" :
        navigator.userAgent.includes("Safari")   ? "safari" : "other";

    const components = [
        navigator.userAgent,
        navigator.language,
        screen.width + "x" + screen.height,
        screen.colorDepth,
        Intl.DateTimeFormat().resolvedOptions().timeZone,
        navigator.platform,
        navigator.hardwareConcurrency,
        navigator.maxTouchPoints,
        browserName    // ← key: detects Chrome vs Edge vs Firefox
    ];

    const str = components.join("|");
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        const char = str.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    return Math.abs(hash).toString(16);
}

// ── Alert Helper ───────────────────────────────────────────────────────────
function showAlert(elementId, message, type = "error") {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = message;
    el.className = `alert ${type}`;
    el.style.display = "block";
    setTimeout(() => { el.style.display = "none"; }, 5000);
}

// ── Token Storage ──────────────────────────────────────────────────────────
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
function requireLogin() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

function redirectIfLoggedIn() {
    if (getToken()) {
        window.location.href = "dashboard.html";
    }
}

// ── API Request Helper ─────────────────────────────────────────────────────
async function apiRequest(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
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