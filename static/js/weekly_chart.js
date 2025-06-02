
document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/top_repeats_weekly");
  const data = await res.json();

  const labels = data.map(d => d.label);
  const repeatCounts = data.map(d => d.repeat_count);
  const tooltips = data.map(d => 
    [`${d.title} - ${d.artist}`,
     `Avg Completion: ${d.avg_completion}%`,
     `${d.week_start} to ${d.week_end}`
    ]
  );

  const ctx = document.getElementById("weeklyChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [{
        label: "Top Weekly Repeat Count",
        data: repeatCounts,
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              return tooltips[context.dataIndex];
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Repeat Count"
          }
        },
        x: {
          title: {
            display: true,
            text: "Week"
          }
        }
      }
    }
  });
});
