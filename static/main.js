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

    const res = await fetch("/predict", { method: "POST", body: fd });
    const data = await res.json();

    showResults(data);
  }

  function showResults(data) {
    loadingState.style.display = "none";
    resultContent.style.display = "block";

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
        </div>
      </div>
    `;
  }

  backToHomeBtn.onclick = () => {
    resultPage.classList.remove("active");
    homePage.classList.add("active");
  };
}
