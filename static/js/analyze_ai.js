document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("ai-analyze-btn");
  const modalEl = document.getElementById("aiAnalyzeModal");
  const modal = new bootstrap.Modal(modalEl);
  const bar = document.getElementById("ai-progress-bar");
  const processed = document.getElementById("ai-processed");
  const total = document.getElementById("ai-total");
  const closeWrapper = document.getElementById("ai-analyze-close-wrapper");

  let interval;

  btn.addEventListener("click", async () => {
    const res = await fetch("/api/analyze_emotion", { method: "POST" });
    const result = await res.json();

    if (!res.ok || !result.request_id) {
      alert(result.error || "Failed to start analysis.");
      return;
    }

    modal.show();
    bar.style.width = "0%";
    processed.textContent = "0";
    total.textContent = "?";
    closeWrapper.classList.add("d-none");

    const requestId = result.request_id;

    interval = setInterval(async () => {
      const r = await fetch(`/api/request_progress?request_id=${requestId}`);
      if (r.status === 404) {
        clearInterval(interval);
        bar.style.width = "100%";
        processed.textContent = total.textContent;
        closeWrapper.classList.remove("d-none");
        return;
      }
      const data = await r.json();
      processed.textContent = data.num_processed;
      total.textContent = data.num_total;
      const percent = data.num_total ? Math.round((data.num_processed / data.num_total) * 100) : 0;
      bar.style.width = percent + "%";
    }, 10000);
  });

  modalEl.addEventListener("hidden.bs.modal", () => clearInterval(interval));
});
