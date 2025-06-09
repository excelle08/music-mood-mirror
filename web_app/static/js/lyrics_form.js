
document.addEventListener("DOMContentLoaded", () => {
  const uploadInput = document.getElementById("history-upload");
  const outputDiv = document.getElementById("lyrics-output");
  const submitBtn = document.getElementById("submit-btn");

  let historyData = [];

  uploadInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const text = await file.text();
    try {
      historyData = JSON.parse(text);
      alert(`Loaded ${historyData.length} entries from file.`);
    } catch (err) {
      alert("Failed to parse JSON.");
    }
  });

  submitBtn.addEventListener("click", async () => {
    if (historyData.length === 0) {
      alert("No data loaded.");
      return;
    }

    const randomEntry = historyData[Math.floor(Math.random() * historyData.length)];

    const response = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(randomEntry)
    });

    const result = await response.json();

    if (response.ok) {
      outputDiv.innerHTML = `
        <h4>Original Metadata</h4>
        <p><strong>Title:</strong> ${result.title}</p>
        <p><strong>Artist:</strong> ${result.artist}</p>
        <p><strong>Album:</strong> ${result.album || "(None)"}</p>
        <h4>Search Result</h4>
        <p><strong>Result Title:</strong> ${result.result_title}</p>
        <p><strong>Result Artist:</strong> ${result.result_artist}</p>
        <p><strong>Result Album:</strong> ${result.result_album}</p>
        <h4>Lyrics</h4>
        <pre>${result.lyrics || "(No lyrics found)"}</pre>
      `;
    } else {
      outputDiv.innerHTML = `<p class="text-danger">Error: ${result.error}</p>`;
    }
  });
});
