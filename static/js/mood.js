
document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/mood");
  const data = await res.json();

  const labels = data.map(d => d.label);
  const scores = data.map(d => d.score);

  const getColor = (score) => {
    const t = (score - 1) / 4; // normalize to 0–1
    const r = Math.round(255 * t);
    const g = 50;
    const b = Math.round(255 * (1 - t));
    return `rgb(${r}, ${g}, ${b})`;
  };

  const pointColors = scores.map(getColor);

  const chart = new Chart(document.getElementById("moodChart").getContext("2d"), {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "Mood Score (1–5)",
        data: scores,
        fill: false,
        borderColor: "rgba(255, 99, 132, 0.5)",
        backgroundColor: pointColors,
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          min: 0,
          max: 5,
          title: {
            display: true,
            text: "Mood Score"
          }
        },
        x: {
          title: {
            display: true,
            text: "Week"
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: context => `Score: ${context.parsed.y}`
          }
        }
      }
    }
  });


  chart.canvas.onclick = function (event) {
      const points = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
      if (points.length > 0) {
          const point = points[0];
          const label = chart.data.labels[point.index]; // label like '2025-W22'
          const [year, week] = label.split('-W').map(Number);

          fetch(`/api/weekly_tags?year=${year}&week=${week}`)
              .then(response => response.json())
              .then(data => renderWordCloud(data))
              .catch(error => console.error('Failed to fetch mood tags:', error));
      }
  };
});


function renderWordCloud(tags) {
    const list = tags.map(([tag, weight]) => [tag, weight]);
    WordCloud(document.getElementById('word-cloud'), {
        list: list,
        gridSize: 10,
        weightFactor: 5,
        fontFamily: 'Times, serif',
        color: 'random-dark',
        backgroundColor: '#f0f0f0'
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const chart = window.moodChart;  // assuming moodChart is globally available
    if (!chart) return;

});
        