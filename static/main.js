const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginEmail").value.trim();
    const password = document.getElementById("loginPassword").value.trim();

    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.error);
      return;
    }

    localStorage.setItem("username", data.username);
    window.location.href = "/home";
  });
}

// ======================
// SIGNUP PAGE
// ======================
const signupForm = document.getElementById("signupForm");

if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("signupUsername").value.trim();
    const email = document.getElementById("signupEmail").value.trim();
    const password = document.getElementById("signupPassword").value.trim();

    const res = await fetch("/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password })
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.error);
      return;
    }

    alert("✔ Account created successfully!");
    window.location.href = "/";
  });
}

// ======================
// HOME + RESULT PAGE
// ======================
if (window.location.pathname === "/home") {

  // Helper function to get username
  function getUsername() {
    return localStorage.getItem("username") || "Guest";
  }

  // Greeting
  const userGreeting = document.getElementById("userGreeting");
  if (userGreeting && getUsername()) {
    userGreeting.textContent = "👋 " + getUsername();
  }

  let currentImage = null;
  let uploadedFile = null;
  let cameraStream = null;

  // ---------- Upload ----------
  const uploadCard = document.getElementById("uploadCard");
  const fileInput = document.getElementById("fileInput");
  const previewSection = document.getElementById("previewSection");
  const imagePreview = document.getElementById("imagePreview");
  const removeImageBtn = document.getElementById("removeImage");

  uploadCard.onclick = () => fileInput.click();

  fileInput.onchange = (e) => {
    const file = e.target.files[0];
    if (file) preview(file);
  };

  // ---------- Store Card ----------
  const storeCard = document.getElementById("storeCard");
  if (storeCard) {
    storeCard.onclick = () => {
      window.location.href = "/store"; // or use the route for your store page
    };
  }

  function preview(file) {
    uploadedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      currentImage = e.target.result;
      imagePreview.src = currentImage;
      previewSection.style.display = "block";
    };
    reader.readAsDataURL(file);
  }

  removeImageBtn.onclick = () => {
    currentImage = null;
    uploadedFile = null;
    previewSection.style.display = "none";
  };

  // ---------- Camera ----------
  const cameraCard = document.getElementById("cameraCard");
  const cameraModal = document.getElementById("cameraModal");
  const closeCameraModal = document.getElementById("closeCameraModal");
  const cancelCameraBtn = document.getElementById("cancelCameraBtn");
  const cameraStreamVideo = document.getElementById("cameraStream");
  const cameraCanvas = document.getElementById("cameraCanvas");
  const captureBtn = document.getElementById("captureBtn");

  cameraCard.onclick = openCamera;

  async function openCamera() {
    try {
      cameraStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" }
      });
      cameraStreamVideo.srcObject = cameraStream;
      cameraModal.classList.add("active");
    } catch (err) {
      alert("Camera not accessible");
    }
  }

  function closeCamera() {
    if (cameraStream) {
      cameraStream.getTracks().forEach(t => t.stop());
    }
    cameraModal.classList.remove("active");
  }

  closeCameraModal.onclick = closeCamera;
  cancelCameraBtn.onclick = closeCamera;

  captureBtn.onclick = () => {
    const ctx = cameraCanvas.getContext("2d");
    cameraCanvas.width = cameraStreamVideo.videoWidth;
    cameraCanvas.height = cameraStreamVideo.videoHeight;

    ctx.drawImage(cameraStreamVideo, 0, 0);

    cameraCanvas.toBlob((blob) => {
      uploadedFile = new File([blob], "camera.jpg", { type: "image/jpeg" });

      const reader = new FileReader();
      reader.onload = (e) => {
        currentImage = e.target.result;
        imagePreview.src = currentImage;
        previewSection.style.display = "block";
      };
      reader.readAsDataURL(blob);
    });

    closeCamera();
  };

  // ---------- Analyze ----------
  const analyzeBtn = document.getElementById("analyzeBtn");
  const homePage = document.getElementById("homePage");
  const resultPage = document.getElementById("resultPage");
  const resultImage = document.getElementById("resultImage");
  const loadingState = document.getElementById("loadingState");
  const resultContent = document.getElementById("resultContent");
  const resultData = document.getElementById("resultData");
  const backToHomeBtn = document.getElementById("backToHomeBtn");

  analyzeBtn.onclick = () => {
    if (!uploadedFile) {
      alert("Please upload or capture an image first.");
      return;
    }

    resultImage.src = currentImage;
    loadingState.style.display = "block";
    resultContent.style.display = "none";

    homePage.classList.remove("active");
    resultPage.classList.add("active");

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => sendPredict(pos.coords.latitude, pos.coords.longitude),
        () => sendPredict(null, null)
      );
    } else {
      sendPredict(null, null);
    }
  };

  async function sendPredict(lat, lng) {
    const fd = new FormData();
    fd.append("file", uploadedFile);
    if (lat && lng) {
      fd.append("lat", lat);
      fd.append("lng", lng);
    }

    try {
      const res = await fetch("/predict", { method: "POST", body: fd });
      const data = await res.json();

      if (!res.ok || !data.success) {
        alert(data.error || "Prediction failed");
        // Go back to home page on error
        backToHomeBtn.click();
        return;
      }

      showResults(data);
    } catch (error) {
      alert("Error: " + error.message);
      backToHomeBtn.click();
    }
  }

  function showResults(data) {
    loadingState.style.display = "none";
    resultContent.style.display = "block";

    // Extract data from new response structure
    const prediction = data.prediction || {};
    const diseaseInfo = data.disease_information || {};
    const fertilizerInfo = data.fertilizer_recommendation || {};
    const storeInfo = data.pesticide_stores || {};
    const recommendations = data.recommendations || {};

    // Disease name
    const diseaseName = diseaseInfo.disease_name || prediction.label || 'Unknown Disease';
    const plantType = diseaseInfo.plant_type || 'Unknown';
    
    // Confidence
    const confidence = prediction.confidence || 0;
    const confidencePercent = prediction.confidence_percentage || (confidence.toFixed(2) + '%');

    // Severity with color coding
    const severity = diseaseInfo.severity || 'Unknown';
    let severityColor = '#666';
    if (severity.toLowerCase().includes('high') || severity.toLowerCase().includes('critical')) {
      severityColor = '#dc3545';
    } else if (severity.toLowerCase().includes('medium')) {
      severityColor = '#ffc107';
    } else if (severity.toLowerCase().includes('none') || severity.toLowerCase().includes('healthy')) {
      severityColor = '#28a745';
    }

    // Build symptoms HTML
    let symptomsHtml = '<p style="color: #666;">No symptoms listed</p>';
    if (diseaseInfo.symptoms && diseaseInfo.symptoms.length > 0) {
      symptomsHtml = '<ul style="margin: 10px 0; padding-left: 20px;">';
      diseaseInfo.symptoms.forEach(symptom => {
        symptomsHtml += `<li style="margin-bottom: 8px; color: #555;">${symptom}</li>`;
      });
      symptomsHtml += '</ul>';
    }

    // Build treatment steps HTML
    let treatmentHtml = '<p style="color: #666;">No treatment steps available</p>';
    if (diseaseInfo.treatment_steps && diseaseInfo.treatment_steps.length > 0) {
      treatmentHtml = '<ol style="margin: 10px 0; padding-left: 20px;">';
      diseaseInfo.treatment_steps.forEach(step => {
        treatmentHtml += `<li style="margin-bottom: 10px; color: #555; line-height: 1.6;">${step}</li>`;
      });
      treatmentHtml += '</ol>';
    }

    // Build recommended products HTML
    let productsHtml = '<p style="color: #666;">No products recommended</p>';
    if (diseaseInfo.recommended_products && diseaseInfo.recommended_products.length > 0) {
      productsHtml = '<ul style="margin: 10px 0; padding-left: 20px;">';
      diseaseInfo.recommended_products.forEach(product => {
        productsHtml += `<li style="margin-bottom: 8px; color: #555;">${product}</li>`;
      });
      productsHtml += '</ul>';
    }

    // Build prevention measures HTML
    let preventionHtml = '<p style="color: #666;">No prevention measures listed</p>';
    if (diseaseInfo.prevention && diseaseInfo.prevention.length > 0) {
      preventionHtml = '<ul style="margin: 10px 0; padding-left: 20px;">';
      diseaseInfo.prevention.forEach(measure => {
        preventionHtml += `<li style="margin-bottom: 8px; color: #555;">${measure}</li>`;
      });
      preventionHtml += '</ul>';
    }

    // Build fertilizer recommendation HTML
    let fertilizerHtml = '';
    if (fertilizerInfo.success && fertilizerInfo.recommendation) {
      const formattedRecommendation = fertilizerInfo.recommendation.replace(/\n/g, '<br>');
      fertilizerHtml = `
        <div style="background: #f8f9ff; padding: 20px; border-radius: 10px; line-height: 1.8; color: #333; border-left: 4px solid #667eea;">
          ${formattedRecommendation}
        </div>
      `;
    } else if (fertilizerInfo.error) {
      fertilizerHtml = `
        <div style="background: #fee; color: #c33; padding: 15px; border-radius: 10px; border-left: 4px solid #c33;">
          ⚠️ ${fertilizerInfo.error}
        </div>
      `;
    } else {
      fertilizerHtml = '<p style="color: #666;">Fertilizer recommendation not available</p>';
    }

    // Build store link HTML
    let storeHtml = '<p style="color: #666;">Store link not available</p>';
    if (storeInfo.bing_maps_link) {
      storeHtml = `
        <a href="${storeInfo.bing_maps_link}" target="_blank" 
           style="display: inline-block; background: #28a745; color: white; padding: 12px 25px; 
                  border-radius: 50px; text-decoration: none; font-size: 1em; transition: all 0.3s;
                  margin-top: 10px;">
          📍 Find Pesticide Stores in Hyderabad
        </a>
        <p style="color: #666; margin-top: 10px; font-size: 0.9em;">
          ${storeInfo.description || 'Click to find stores near you'}
        </p>
      `;
    }

    // Build immediate actions HTML (if available)
    let immediateActionsHtml = '';
    if (recommendations.immediate_action && recommendations.immediate_action.length > 0) {
      immediateActionsHtml = `
        <div class="result-item" style="background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; margin-bottom: 20px; border-radius: 8px;">
          <div class="result-label" style="color: #856404; font-weight: bold; margin-bottom: 10px;">
            ⚡ Immediate Actions Required
          </div>
          <ol style="margin: 10px 0; padding-left: 20px; color: #856404;">
            ${recommendations.immediate_action.map(action => `<li style="margin-bottom: 8px;">${action}</li>`).join('')}
          </ol>
        </div>
      `;
    }

    // Build the complete result HTML
    resultData.innerHTML = `
      ${immediateActionsHtml}

      <div class="result-item">
        <div class="result-label">Disease</div>
        <div class="result-value" style="font-size: 1.3em; color: #333; font-weight: bold;">
          ${diseaseName}
          <div style="font-size: 0.8em; color: #666; font-weight: normal; margin-top: 5px;">
            Plant Type: ${plantType}
          </div>
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">Confidence</div>
        <div class="result-value" style="font-size: 1.2em; color: #667eea; font-weight: bold;">
          ${confidencePercent}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">Severity Level</div>
        <div class="result-value" style="font-size: 1.1em; color: ${severityColor}; font-weight: bold;">
          ${severity}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">🔍 Symptoms</div>
        <div class="result-value">
          ${symptomsHtml}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">💊 Treatment Steps</div>
        <div class="result-value">
          ${treatmentHtml}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">🧪 Recommended Products</div>
        <div class="result-value">
          ${productsHtml}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">🛡️ Prevention Measures</div>
        <div class="result-value">
          ${preventionHtml}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">🌱 Brief Overview of Fertilizer Recommendation</div>
        <div class="result-value">
          ${fertilizerHtml}
        </div>
      </div>

      <div class="result-item">
        <div class="result-label">🏪 Pesticide Stores</div>
        <div class="result-value">
          ${storeHtml}
        </div>
      </div>
    `;
  }

  backToHomeBtn.onclick = () => {
    resultPage.classList.remove("active");
    homePage.classList.add("active");
  };
}