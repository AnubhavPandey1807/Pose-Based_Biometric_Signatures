let videoStream = null;
let capturedFrames = [];

const video = document.getElementById("video");

/* ---------- CAMERA ---------- */
async function startCamera() {
  if (videoStream) return;

  try {
    videoStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 },
      audio: false
    });

    video.srcObject = videoStream;
    await video.play();
  } catch (err) {
    alert("Camera access denied or unavailable");
    console.error(err);
  }
}

/* ---------- POSE CAPTURE ---------- */
async function capturePose(mode) {
  await startCamera(); // 🔥 REQUIRED

  capturedFrames = [];

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");

  for (let i = 0; i < 10; i++) {
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const blob = await new Promise(resolve =>
      canvas.toBlob(resolve, "image/jpeg")
    );

    capturedFrames.push(blob);
    await new Promise(r => setTimeout(r, 200));
  }

  alert("Pose captured successfully");
}

/* ---------- REGISTER ---------- */
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (capturedFrames.length === 0) {
      alert("Capture pose first");
      return;
    }

    const formData = new FormData(registerForm);
    capturedFrames.forEach((f, i) =>
      formData.append("frames", f, `frame_${i}.jpg`)
    );

    const res = await fetch("/auth/register", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (res.ok) {
      alert("Registration successful");
      window.location.href = "/";
    } else {
      alert(data.detail || "Registration failed");
    }
  });
}

/* ---------- LOGIN ---------- */
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (capturedFrames.length === 0) {
      alert("Capture pose first");
      return;
    }

    const formData = new FormData(loginForm);
    capturedFrames.forEach((f, i) =>
      formData.append("frames", f, `frame_${i}.jpg`)
    );

    const res = await fetch("/auth/login", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (res.ok) {
      window.location.href = "/dashboard";
    } else {
      alert(data.detail || "Authentication failed");
    }
  });
}
