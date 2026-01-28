/**
 * Analysis & File Upload Module
 */

const API_BASE = "https://mhenga-crop-bot.onrender.com";

let selectedFile = null;
let resultsView = null;
let fileInfo = null;
let analyzeButton = null;

/**
 * Initialize analyze module
 */
function initAnalyze() {
  console.log("initAnalyze() called");
  
  // Get DOM Elements (ensure they exist)
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("fileInput");
  fileInfo = document.getElementById("file-info");
  analyzeButton = document.getElementById("analyze-button");
  resultsView = document.getElementById("results-view");
  
  // Safety check - if elements don't exist, return
  if (!dropZone || !fileInput || !analyzeButton) {
    console.error("Analyze module: Required DOM elements not found", {
      dropZone: !!dropZone,
      fileInput: !!fileInput,
      fileInfo: !!fileInfo,
      analyzeButton: !!analyzeButton,
      resultsView: !!resultsView
    });
    return;
  }
  
  console.log("Analyze module: All DOM elements found, attaching listeners");
  
  // File input change handler - this fires when a file is selected
  fileInput.addEventListener("change", (e) => {
    console.log("File input changed", e.target.files[0]);
    if (e.target.files[0]) {
      handleFile(e.target.files[0], fileInfo, analyzeButton);
    }
  });
  
  // Drop zone click - open file picker
  dropZone.addEventListener("click", (e) => {
    console.log("Drop zone clicked, opening file picker");
    fileInput.click();
  });
  
  // Drag handlers
  dropZone.addEventListener("dragenter", (e) => handleDragEnter(e, dropZone));
  dropZone.addEventListener("dragover", (e) => handleDragOver(e, dropZone));
  dropZone.addEventListener("dragleave", (e) => handleDragLeave(e, dropZone));
  dropZone.addEventListener("drop", (e) => handleDrop(e, dropZone, fileInput, fileInfo, analyzeButton));

  // Analyze button
  analyzeButton.addEventListener("click", () => {
    console.log("Analyze button clicked");
    handleAnalyzeClick(analyzeButton);
  });
  
  console.log("Analyze module: Initialization complete");
}


/**
 * Handle file selection
 */
function handleFile(file, fileInfo, analyzeButton) {
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    alert("Please upload an image file.");
    return;
  }
  selectedFile = file;
  fileInfo.textContent = `Selected file: ${file.name}`;
  fileInfo.classList.remove("hidden");
  analyzeButton.disabled = false;
}

/**
 * Handle drag enter
 */
function handleDragEnter(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.add("bg-green-50");
}

/**
 * Handle drag over
 */
function handleDragOver(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  e.dataTransfer.dropEffect = "copy";
  dropZone.classList.add("bg-green-50");
}

/**
 * Handle drag leave
 */
function handleDragLeave(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("bg-green-50");
}

/**
 * Handle drop
 */
function handleDrop(e, dropZone, fileInput, fileInfo, analyzeButton) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("bg-green-50");
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    handleFile(files[0], fileInfo, analyzeButton);
  }
}

/**
 * Handle analyze button click
 */
async function handleAnalyzeClick(analyzeButton) {
  if (!selectedFile) return alert("Please upload an image");

  const location = prompt("Enter location (e.g., Nairobi):", "Nairobi");
  if (!location) return alert("Location is required");

  let lat, lon;
  try {
    const geoRes = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(location)}`
    );
    const geoData = await geoRes.json();
    if (!geoData.length) throw new Error("Location not found");
    lat = geoData[0].lat;
    lon = geoData[0].lon;
  } catch (err) {
    return alert("Error getting coordinates: " + err.message);
  }

  const formData = new FormData();
  formData.append("file", selectedFile);
  formData.append("lat", lat);
  formData.append("lon", lon);

  try {
    const token = localStorage.getItem("token");
    console.log("Sending analyze request with file:", selectedFile.name);
    const res = await fetch(API_BASE + "/analyze", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + token
      },
      body: formData
    });
    const data = await res.json();
    console.log("Analyze response:", res.status, data);
    if (!res.ok) {
      const error = data.error || "Analysis failed";
      console.error("Analysis error:", error);
      throw new Error(error);
    }

    console.log("Analysis successful, displaying results");
    displayResults(data);
  } catch (err) {
    console.error("Analyze error caught:", err);
    alert("Error: " + err.message);
  }
}

/**
 * Display analysis results
 */
function displayResults(data) {
  resultsView.classList.remove("hidden");
  resultsView.innerHTML = `
    <div class="space-y-4">
      <div class="bg-green-50 p-4 rounded-lg">
        <h2 class="text-xl font-bold text-green-700 mb-2">Detected Crop</h2>
        <p><strong>English Name:</strong> ${data.cropEnglishName || "Unknown"}</p>
        <p><strong>Scientific Name:</strong> <em>${data.cropScientificName || "Unknown"}</em></p>
      </div>

      <div class="bg-red-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-red-600 mb-2">Disease: ${data.diseaseName}</h3>
        <p>${data.diseaseDescription}</p>
      </div>

      <div class="bg-blue-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-blue-700 mb-2">Prevention</h3>
        <p>${(data.prevention && data.prevention.join(", ")) || "No prevention tips available"}</p>
      </div>

      <div class="bg-orange-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-orange-600 mb-2">Control/Cure</h3>
        <p>${(data.control && data.control.join(", ")) || "No cure info available"}</p>
      </div>

      <div class="bg-green-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-green-700 mb-2">Planting Recommendation</h3>
        <p><strong>${data.recommendation}</strong></p>
      </div>

      <div class="bg-gray-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Weather Information</h3>
        <p><strong>Weather:</strong> ${data.weather}</p>
        <p><strong>Temperature:</strong> ${data.temperature_celsius}°C</p>
        <p><strong>Location:</strong> ${data.location}</p>
      </div>
    </div>
  `;
}

// Initialize is called after login from auth.js
