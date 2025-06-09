
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("analyze-btn");
  const modalEl = document.getElementById("analyzeModal");
  const modal = new bootstrap.Modal(modalEl);
  const bar = document.getElementById("analyze-progress-bar");
  const processed = document.getElementById("analyze-processed");
  const total = document.getElementById("analyze-total");
  const closeWrapper = document.getElementById("analyze-close-wrapper");
  const closeBtn = document.getElementById("analyze-close-btn");

  let interval;

  btn.addEventListener("click", async () => {
    const res = await fetch("/api/analyze_history", { method: "POST" });
    const result = await res.json();

    if (!res.ok || !result.request_id) {
      alert("Failed to start analysis.");
      return;
    }

    modal.show();
    bar.style.width = "0%";
    processed.textContent = "0";
    total.textContent = "?";
    closeWrapper.classList.add("d-none");

    const requestId = result.request_id;

    interval = setInterval(async () => {
      const res = await fetch(`/api/request_progress?request_id=${requestId}`);
      const data = await res.json();

      if (res.status === 404 || data.num_processed === data.num_total) {
        clearInterval(interval);
        bar.style.width = "100%";
        processed.textContent = total.textContent;
        closeWrapper.classList.remove("d-none");
        return;
      }

      processed.textContent = data.num_processed;
      total.textContent = data.num_total;
      const percent = data.num_total ? Math.round((data.num_processed / data.num_total) * 100) : 0;
      bar.style.width = percent + "%";
    }, 1000);
  });

  modalEl.addEventListener("hidden.bs.modal", () => clearInterval(interval));
  closeBtn.addEventListener("click", () => {
    modal.hide();
    clearInterval(interval);
    location.reload();
  });
});
