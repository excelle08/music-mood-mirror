
document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/histograms");
  const data = await res.json();

  // Completion rate histogram
  const completionLabels = [...Array(11)].map((_, i) =>
    i === 10 ? "100%" : `${i * 10}–${(i + 1) * 10 - 1}%`
  );

  new Chart(document.getElementById("completionHistogram").getContext("2d"), {
    type: "bar",
    data: {
      labels: completionLabels,
      datasets: [{
        label: "Count",
        data: data.completion_rate,
        backgroundColor: "rgba(75, 192, 192, 0.5)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Completion Rate Histogram"
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });

  // Seconds played histogram
  const secondsLabels = [...Array(13)].map((_, i) =>
    i === 12 ? "360s+" : `${i * 30}–${(i + 1) * 30 - 1}s`
  );

  new Chart(document.getElementById("secondsHistogram").getContext("2d"), {
    type: "bar",
    data: {
      labels: secondsLabels,
      datasets: [{
        label: "Count",
        data: data.seconds_played,
        backgroundColor: "rgba(255, 99, 132, 0.5)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1
      }]
    },
    options: {
      plugins: {
        title: {
          display: true,
          text: "Seconds Played Histogram"
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
});
