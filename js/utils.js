/**
 * Utility Functions
 */

const API_BASE = "https://mhenga-crop-bot.onrender.com";

/**
 * Format temperature for display
 */
function formatTemperature(celsius) {
  return `${parseFloat(celsius).toFixed(1)}°C`;
}

/**
 * Format location string
 */
function formatLocation(lat, lon) {
  return `${parseFloat(lat).toFixed(4)}, ${parseFloat(lon).toFixed(4)}`;
}

/**
 * Show loading state on button
 */
function setButtonLoading(button, isLoading) {
  if (isLoading) {
    button.disabled = true;
    button.textContent = "Loading...";
    button.classList.add("opacity-50");
  } else {
    button.disabled = false;
    button.textContent = "Analyze";
    button.classList.remove("opacity-50");
  }
}

/**
 * Show error notification
 */
function showError(message) {
  const notification = document.createElement("div");
  notification.className = "fixed top-4 right-4 bg-red-500 text-white px-4 py-3 rounded-lg shadow-lg";
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 5000);
}

/**
 * Show success notification
 */
function showSuccess(message) {
  const notification = document.createElement("div");
  notification.className = "fixed top-4 right-4 bg-green-500 text-white px-4 py-3 rounded-lg shadow-lg";
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.remove(), 5000);
}

/**
 * Get token from localStorage
 */
function getToken() {
  return localStorage.getItem("token");
}

/**
 * Get user from localStorage
 */
function getUser() {
  return JSON.parse(localStorage.getItem("user") || "null");
}

/**
 * Check if user is authenticated
 */
function isAuthenticated() {
  return getToken() !== null;
}
