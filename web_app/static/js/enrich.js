
document.addEventListener("DOMContentLoaded", () => {
  const enrichBtn = document.getElementById("enrich-btn");
  const modalEl = document.getElementById("progressModal");
  const modal = new bootstrap.Modal(modalEl);
  const processedSpan = document.getElementById("processed-count");
  const totalSpan = document.getElementById("total-count");
  const successSpan = document.getElementById("success-count");
  const progressBar = document.getElementById("progress-bar");
  const closeBtn = document.getElementById("modal-close-btn");

  let pollInterval;

  const stopPolling = () => {
    clearInterval(pollInterval);
    closeBtn.classList.remove("d-none");
  };

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
    progressBar.style.width = "0%";
    closeBtn.classList.add("d-none");

    const requestId = result.request_id;

    pollInterval = setInterval(async () => {
      const res = await fetch(`/api/request_progress?request_id=${requestId}`);
      const data = await res.json();

      if (res.status === 404 || (data.num_processed === data.num_total && data.num_total > 0)) {
        stopPolling();
        progressBar.style.width = "100%";
        processedSpan.textContent = totalSpan.textContent;
        closeBtn.classList.remove("d-none");
        return;
      }

      processedSpan.textContent = data.num_processed;
      totalSpan.textContent = data.num_total;
      successSpan.textContent = data.num_successful;

      const percent = data.num_total ? Math.round((data.num_processed / data.num_total) * 100) : 0;
      progressBar.style.width = percent + "%";
    }, 1000);
  });

  modalEl.addEventListener("hidden.bs.modal", () => {
    clearInterval(pollInterval);
  });

  closeBtn.addEventListener("click", () => {
    modal.hide();
    location.reload();
  });
});
