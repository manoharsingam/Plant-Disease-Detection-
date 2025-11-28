<<<<<<< HEAD
// // ======================
// // LOGIN PAGE
// // ======================
// const loginForm = document.getElementById("loginForm");

// if (loginForm) {
//   loginForm.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     const email = document.getElementById("loginEmail").value.trim();
//     const password = document.getElementById("loginPassword").value.trim();

//     const res = await fetch("/api/login", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ email, password })
//     });

//     const data = await res.json();

//     if (!res.ok) {
//       alert(data.error);
//       return;
//     }

//     localStorage.setItem("username", data.username);
//     window.location.href = "/home";
//   });
// }

// // ======================
// // SIGNUP PAGE
// // ======================
// const signupForm = document.getElementById("signupForm");

// if (signupForm) {
//   signupForm.addEventListener("submit", async (e) => {
//     e.preventDefault();

//     const username = document.getElementById("signupUsername").value.trim();
//     const email = document.getElementById("signupEmail").value.trim();
//     const password = document.getElementById("signupPassword").value.trim();

//     const res = await fetch("/api/signup", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ username, email, password })
//     });

//     const data = await res.json();

//     if (!res.ok) {
//       alert(data.error);
//       return;
//     }

//     alert("Account created successfully!");
//     window.location.href = "/";
//   });
// }

// // ======================
// // HOME PAGE
// // ======================
// if (window.location.pathname === "/home") {

//   document.getElementById("userGreeting").textContent =
//     localStorage.getItem("username");

//   let currentImage = null;
//   let uploadedFile = null;

//   // ---------- Upload ----------
//   document.getElementById("uploadCard").onclick = () =>
//     document.getElementById("fileInput").click();

//   document.getElementById("fileInput").onchange = (e) => {
//     const file = e.target.files[0];
//     if (file) preview(file);
//   };

//   function preview(file) {
//     uploadedFile = file;
//     const reader = new FileReader();

//     reader.onload = (e) => {
//       currentImage = e.target.result;
//       document.getElementById("imagePreview").src = currentImage;
//       document.getElementById("previewSection").style.display = "block";
//     };

//     reader.readAsDataURL(file);
//   }

//   document.getElementById("removeImage").onclick = () => {
//     currentImage = null;
//     uploadedFile = null;
//     document.getElementById("previewSection").style.display = "none";
//   };

//   // ---------- Camera ----------
//   let cameraStream = null;

//   document.getElementById("cameraCard").onclick = openCamera;

//   async function openCamera() {
//     const modal = document.getElementById("cameraModal");
//     const video = document.getElementById("cameraStream");

//     try {
//       cameraStream = await navigator.mediaDevices.getUserMedia({
//         video: { facingMode: "environment" }
//       });

//       video.srcObject = cameraStream;
//       modal.classList.add("active");
//     } catch (err) {
//       alert("Camera not accessible");
//     }
//   }

//   document.getElementById("closeCameraModal").onclick =
//   document.getElementById("cancelCameraBtn").onclick = closeCamera;

//   function closeCamera() {
//     if (cameraStream) {
//       cameraStream.getTracks().forEach(t => t.stop());
//     }
//     document.getElementById("cameraModal").classList.remove("active");
//   }

//   document.getElementById("captureBtn").onclick = () => {
//     const video = document.getElementById("cameraStream");
//     const canvas = document.getElementById("cameraCanvas");
//     const ctx = canvas.getContext("2d");

//     canvas.width = video.videoWidth;
//     canvas.height = video.videoHeight;

//     ctx.drawImage(video, 0, 0);

//     canvas.toBlob((blob) => {
//       uploadedFile = new File([blob], "camera.jpg", { type: "image/jpeg" });

//       const reader = new FileReader();
//       reader.onload = (e) => {
//         currentImage = e.target.result;
//         document.getElementById("imagePreview").src = currentImage;
//         document.getElementById("previewSection").style.display = "block";
//       };

//       reader.readAsDataURL(blob);
//     });

//     closeCamera();
//   };

//   // ---------- Analyze ----------
//   document.getElementById("analyzeBtn").onclick = async () => {
//     document.getElementById("resultImage").src = currentImage;

//     const fd = new FormData();
//     fd.append("file", uploadedFile);

//     const res = await fetch("/predict", { method: "POST", body: fd });
//     const data = await res.json();

//     showResults(data);
//   };

//   function showResults(data) {
//     document.getElementById("loadingState").style.display = "none";
//     document.getElementById("resultContent").style.display = "block";

//     let top3 = data.top3.map(
//       i => `${i.label} (${(i.confidence * 100).toFixed(1)}%)`
//     ).join(", ");

//     document.getElementById("resultData").innerHTML = `
//       <p><b>Disease:</b> ${data.label}</p>
//       <p><b>Confidence:</b> ${(data.confidence * 100).toFixed(2)}%</p>
//       <p><b>Top 3:</b> ${top3}</p>
//       <p><b>Recommendation:</b><br>${data.ai_recommendation}</p>
//       <p><b>Pesticide Stores:</b><br>
//          <a href="${data.map_link}" target="_blank">Open in Maps</a></p>
//     `;

//     document.getElementById("homePage").classList.remove("active");
//     document.getElementById("resultPage").classList.add("active");
//   }

//   document.getElementById("backToHomeBtn").onclick = () => {
//     document.getElementById("resultPage").classList.remove("active");
//     document.getElementById("homePage").classList.add("active");
//   };
// }



// ======================
// HELPER FUNCTIONS
// ======================
function getUsername() {
  return localStorage.getItem("username");
}

// ======================
// LOGIN PAGE
// ======================
=======
>>>>>>> friend/main
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

<<<<<<< HEAD
=======
  // Helper function to get username
  function getUsername() {
    return localStorage.getItem("username") || "Guest";
  }

>>>>>>> friend/main
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

<<<<<<< HEAD
=======
  // ---------- Store Card ----------
  const storeCard = document.getElementById("storeCard");
  if (storeCard) {
    storeCard.onclick = () => {
      window.location.href = "/store"; // or use the route for your store page
    };
  }

>>>>>>> friend/main
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

<<<<<<< HEAD
    const res = await fetch("/predict", { method: "POST", body: fd });
    const data = await res.json();

    showResults(data);
=======
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
>>>>>>> friend/main
  }

  function showResults(data) {
    loadingState.style.display = "none";
    resultContent.style.display = "block";

<<<<<<< HEAD
    let dealersHtml = "<p>No nearby fertilizer dealers found.</p>";

    if (data.dealers && data.dealers.length > 0) {
      dealersHtml = data.dealers
        .map(d => `
          <div class="result-item">
            <div class="result-label">${d.name || "Dealer"}</div>
            <div class="result-value">
              ${d.address ? "📍 " + d.address + "<br>" : ""}
              ${d.phone ? "📞 " + d.phone + "<br>" : ""}
              ${d.maps_url ? `<a href="${d.maps_url}" target="_blank">Open in Google Maps</a>` : ""}
            </div>
          </div>
        `)
        .join("");
    }

    resultData.innerHTML = `
      <div class="result-item">
        <div class="result-label">Disease</div>
        <div class="result-value">${data.label}</div>
      </div>
      <div class="result-item">
        <div class="result-label">Confidence</div>
        <div class="result-value">${(data.confidence * 100).toFixed(2)}%</div>
      </div>
      <div class="result-item">
        <div class="result-label">AI Recommendation</div>
        <div class="result-value">${data.ai_recommendation}</div>
      </div>
      <div class="result-item">
        <div class="result-label">Nearby Fertilizer Dealers</div>
        <div class="result-value">
          ${dealersHtml}
=======
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
>>>>>>> friend/main
        </div>
      </div>
    `;
  }

  backToHomeBtn.onclick = () => {
    resultPage.classList.remove("active");
    homePage.classList.add("active");
  };
<<<<<<< HEAD
}
=======
}
>>>>>>> friend/main
