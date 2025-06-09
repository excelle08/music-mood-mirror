
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("upload-form");
  const modalEl = document.getElementById("progressModal");
  const modal = new bootstrap.Modal(modalEl);
  const processedSpan = document.getElementById("processed-count");
  const totalSpan = document.getElementById("total-count");
  const successSpan = document.getElementById("success-count");
  const progressBar = document.getElementById("progress-bar");
  const closeBtn = document.getElementById("modal-close-btn");
  const closeWrapper = document.getElementById("modal-close-btn-wrapper");

  let pollInterval;

  const stopPolling = () => {
    clearInterval(pollInterval);
    closeBtn.classList.remove("d-none");
  };

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const fileInput = document.getElementById("history_file");
    const formData = new FormData();
    formData.append("history_file", fileInput.files[0]);

    const res = await fetch("/api/upload_history", {
      method: "POST",
      body: formData
    });

    const result = await res.json();
    if (!res.ok || !result.request_id) {
      alert("Failed to start upload.");
      return;
    }

    modal.show();
    processedSpan.textContent = "0";
    totalSpan.textContent = "?";
    successSpan.textContent = "0";
    progressBar.style.width = "0%";
    closeWrapper.classList.add("d-none");

    const requestId = result.request_id;

    pollInterval = setInterval(async () => {
      const res = await fetch(`/api/request_progress?request_id=${requestId}`);
      const data = await res.json();

      if (res.status === 404 || (data.num_processed === data.num_total && data.num_total > 0)) {
        console.log("Stopping polling, either not found or completed.");
        console.log(data);
        console.log(res.status);
        stopPolling();
        progressBar.style.width = "100%";
        processedSpan.textContent = totalSpan.textContent;
        closeWrapper.classList.remove("d-none");
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
    location.href = "/view_history";
  });
});
