
document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/top_repeats_weekly");
  const data = await res.json();

  const labelSet = [...new Set(data.map(d => d.label))];

  const grouped = { 1: {}, 2: {}, 3: {} };
  const tooltips = { 1: {}, 2: {}, 3: {} };

  for (const row of data) {
    grouped[row.rank][row.label] = row.repeat_count;
    tooltips[row.rank][row.label] = [
      `${row.title} - ${row.artist}`,
      `Avg Completion: ${row.avg_completion}%`,
      `${row.week_start} to ${row.week_end}`
    ];
  }

  const datasets = [1, 2, 3].map(rank => ({
    label: `Top ${rank}`,
    data: labelSet.map(l => grouped[rank][l] || 0),
    backgroundColor: rank === 1 ? 'rgba(54, 162, 235, 0.5)' :
                     rank === 2 ? 'rgba(255, 159, 64, 0.5)' :
                     'rgba(153, 102, 255, 0.5)',
    borderColor: rank === 1 ? 'rgba(54, 162, 235, 1)' :
                 rank === 2 ? 'rgba(255, 159, 64, 1)' :
                 'rgba(153, 102, 255, 1)',
    borderWidth: 1
  }));

  const ctx = document.getElementById("weeklyChart").getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: labelSet,
      datasets: datasets
    },
    options: {
      responsive: true,
      interaction: {
        mode: "nearest",
        axis: "x",
        intersect: false
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function(context) {
              const rank = context.dataset.label.split(" ")[1];
              const week = context.label;
              return tooltips[rank][week] || "(no data)";
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
