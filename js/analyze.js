let selectedFile = null;
let resultsView = null;
let fileInfo = null;
let analyzeButton = null;
let analyzeHandler = null;

function initAnalyze() {
  console.log("initAnalyze() called");
  const dropZone = document.getElementById("drop-zone");
  const fileInput = document.getElementById("fileInput");
  fileInfo = document.getElementById("file-info");
  analyzeButton = document.getElementById("analyze-button");
  resultsView = document.getElementById("results-view");
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
  fileInput.addEventListener("change", (e) => {
    console.log("File input changed", e.target.files[0]);
    if (e.target.files[0]) {
      handleFile(e.target.files[0], fileInfo, analyzeButton);
    }
  });
  dropZone.addEventListener("click", (e) => {
    console.log("Drop zone clicked, opening file picker");
    fileInput.click();
  });
  dropZone.addEventListener("dragenter", (e) => handleDragEnter(e, dropZone));
  dropZone.addEventListener("dragover", (e) => handleDragOver(e, dropZone));
  dropZone.addEventListener("dragleave", (e) => handleDragLeave(e, dropZone));
  dropZone.addEventListener("drop", (e) => handleDrop(e, dropZone, fileInput, fileInfo, analyzeButton));
  if (analyzeHandler) {
    analyzeButton.removeEventListener("click", analyzeHandler);
  }
  analyzeHandler = () => {
    console.log("Analyze button clicked");
    handleAnalyzeClick(analyzeButton);
  };
  analyzeButton.addEventListener("click", analyzeHandler);
  console.log("Analyze module: Initialization complete");
}

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

  setTimeout(() => {
    if (!analyzeButton.disabled) {
      analyzeButton.click();
    }
  }, 0);
}

function handleDragEnter(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.add("bg-green-50");
}

function handleDragOver(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  e.dataTransfer.dropEffect = "copy";
  dropZone.classList.add("bg-green-50");
}

function handleDragLeave(e, dropZone) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("bg-green-50");
}

function handleDrop(e, dropZone, fileInput, fileInfo, analyzeButton) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove("bg-green-50");
  const files = e.dataTransfer.files;
  if (files && files.length > 0) {
    handleFile(files[0], fileInfo, analyzeButton);
  }
}

async function handleAnalyzeClick(analyzeButton) {
  if (!selectedFile) return alert("Please upload an image");

  if (typeof setButtonLoading === 'function') {
    setButtonLoading(analyzeButton, true);
  } else {
    analyzeButton.disabled = true;
  }

  const location = prompt("Enter location (e.g., Nairobi):", "Nairobi");
  if (!location) {
    if (typeof setButtonLoading === 'function') {
      setButtonLoading(analyzeButton, false);
    } else {
      analyzeButton.disabled = false;
    }
    return alert("Location is required");
  }

  const userCrop = prompt("If you know the crop, enter its name (e.g. maize, tomato) or leave blank:", "");

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
  if (userCrop) {
    formData.append("crop", userCrop);
  }

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
  } finally {
    if (typeof setButtonLoading === 'function') {
      setButtonLoading(analyzeButton, false);
    } else {
      analyzeButton.disabled = false;
    }
  }
}

function displayResults(data) {
  resultsView.classList.remove("hidden");
  let predictionSection = "";
  if (data.all_predictions && data.all_predictions.length) {
    predictionSection = `<div class="bg-yellow-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-yellow-700 mb-2">Model suggestions</h3>
        <ul>
          ${data.all_predictions.map(p => `
            <li>${p.class} (${(p.confidence * 100).toFixed(1)}% confidence)${p.crop_matches ? " &mdash; matches crop" : ""}</li>
          `).join("")}
        </ul>
      </div>`;
  }

  resultsView.innerHTML = `
    <div class="space-y-4">
      <div class="bg-green-50 p-4 rounded-lg">
        <h2 class="text-xl font-bold text-green-700 mb-2">Detected Crop</h2>
        <p><strong>English Name:</strong> ${data.cropEnglishName || "Unknown"}</p>
        <p><strong>Scientific Name:</strong> <em>${data.cropScientificName || "Unknown"}</em></p>
      </div>

      ${predictionSection}

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

      ${data.recommendation_summary ? `
      <div class="bg-indigo-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-indigo-700 mb-2">Recommendations</h3>
        ${data.recommendation_summary.split("\n").map(line => `<p class="mb-1">${line}</p>`).join("")}
      </div>
      ` : ""}

      <div class="bg-gray-50 p-4 rounded-lg">
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Weather Information</h3>
        <p><strong>Weather:</strong> ${data.weather}</p>
        <p><strong>Temperature:</strong> ${data.temperature_celsius}°C</p>
        <p><strong>Location:</strong> ${data.location}</p>
      </div>
      
      <button id="analyze-another" class="w-full mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
        Analyze Another Image
      </button>
    </div>
  `;
  document.getElementById("analyze-another").addEventListener("click", resetAnalyzeForm);
}

function resetAnalyzeForm() {
  selectedFile = null;
  const fileInput = document.getElementById("fileInput");
  fileInput.value = "";
  fileInfo.classList.add("hidden");
  fileInfo.textContent = "";
  analyzeButton.disabled = true;
  resultsView.classList.add("hidden");
  resultsView.innerHTML = "";
}

