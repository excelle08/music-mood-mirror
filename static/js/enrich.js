document.addEventListener("DOMContentLoaded", () => {
  const enrichBtn = document.getElementById("enrich-btn");
  const modal = new bootstrap.Modal(document.getElementById("progressModal"));
  const processedSpan = document.getElementById("processed-count");
  const totalSpan = document.getElementById("total-count");
  const successSpan = document.getElementById("success-count");

  let pollInterval;

  enrichBtn.addEventListener("click", async () => {
    const response = await fetch("/api/enrich_lyrics", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const result = await response.json();
    if (!response.ok || !result.request_id) {
      alert("Failed to start enrichment.");
      return;
    }

    modal.show();
    processedSpan.textContent = "0";
    totalSpan.textContent = "?";
    successSpan.textContent = "0";

    const requestId = result.request_id;

    pollInterval = setInterval(async () => {
      const res = await fetch(`/api/request_progress?request_id=${requestId}`);
      const data = await res.json();
      if (data.error) return;

      processedSpan.textContent = data.num_processed;
      totalSpan.textContent = data.num_total;
      successSpan.textContent = data.num_successful;

      if (data.num_processed >= data.num_total) {
        clearInterval(pollInterval);
        setTimeout(() => {
          modal.hide();
          location.reload();
        }, 1000);
      }
    }, 1000);
  });
});
