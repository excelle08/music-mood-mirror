// Mood tag cache
const moodTagCache = {};

const positivityColors = {
    'Joyful': '#ff4d4d',
    'Melancholic': '#6699cc',
    'Hopeful': '#ff9933',
    'Angry': '#990000',
    'Romantic': '#ff66b2',
    'Nostalgic': '#9966cc',
    'Sad': '#336699',
    'Energetic': '#ff6600',
    'Passionate': '#ff5050',
    'Lonely': '#333366',
    'Uplifting': '#ffcc00',
    'Bittersweet': '#cc9966',
    'Empowering': '#66cc00',
    'Heartbroken': '#660033',
    'Reflective': '#999999',
    'Playful': '#ffcc66',
    'Dark': '#000000',
    'Calm': '#66cccc',
    'Longing': '#666699',
    'Triumphant': '#33cc33'
};

function getColor(word) {
    return positivityColors[word] || null;
}

// Inject animation styles if not already present
function injectAnimationStyles() {
    if (document.getElementById('wordcloud-animation-style')) return;

    const style = document.createElement('style');
    style.id = 'wordcloud-animation-style';
    style.innerHTML = `
        @keyframes flyin {
            0% {
                opacity: 0;
                transform: translateY(-30px) scale(0.8);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        #word-cloud span {
            display: inline-block;
            opacity: 0;
            animation: flyin 0.6s ease forwards;
        }
        @keyframes flyout {
            0% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
            100% {
                opacity: 0;
                transform: translateY(-40px) scale(0.7);
            }
        }
        #word-cloud span.fly-out {
            animation: flyout 0.5s ease forwards;
        }
    `;
    document.head.appendChild(style);
}

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
          const label = chart.data.labels[point.index]; // '2025-W22'
          const [year, week] = label.split('-W').map(Number);

          const cacheKey = `${year}-W${week}`;
          if (moodTagCache[cacheKey]) {
              renderWordCloud(moodTagCache[cacheKey]);
              return;
          }

          fetch(`/api/weekly_tags?year=${year}&week=${week}`)
              .then(response => response.json())
              .then(data => {
                  moodTagCache[cacheKey] = data;
                  renderWordCloud(data);
              })
              .catch(error => console.error('Failed to fetch mood tags:', error));
      }
  };

    /*
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
  */
});

function animateOldWordsOut(callback) {
    const oldWords = document.querySelectorAll('#word-cloud span');
    if (oldWords.length === 0) {
        callback();
        return;
    }

    oldWords.forEach((el, i) => {
        el.classList.add('fly-out');
        el.style.animationDelay = (i * 10) + 'ms';
    });

    setTimeout(() => {
        callback();
    }, 600); // Allow fly-out animation to complete
}

function renderWordCloud(tags) {
    const container = document.getElementById('word-cloud');
    // container.innerHTML = '';
    animateOldWordsOut(() => {
      container.innerHTML = '';
      // then call WordCloud() here

      container.style.opacity = 0;

      const maxWeight = Math.max(...tags.map(([_, w]) => w));
      const width = container.offsetWidth;

      // Scale weight factor based on container width and weight range
      const baseFactor = width / 5;
      const factor = maxWeight > 0 ? baseFactor / maxWeight : 10;

      WordCloud(container, {
          list: tags,
          gridSize: Math.round(width / 100),
          weightFactor: factor,
          fontFamily: 'Segoe UI, sans-serif',
          color: function(word) {
              return getColor(word) || (['#3e3e3e', '#5c5c8a', '#666699', '#336666', '#666633'][Math.floor(Math.random() * 5)]);
          },
          backgroundColor: '#ffffff',
          rotateRatio: 0.2,
          shuffle: true,
          drawOutOfBound: false
      });

      setTimeout(() => {
          container.style.transition = 'opacity 0.6s ease-in';
          container.style.opacity = 1;
      }, 200);

      setTimeout(() => {
          injectAnimationStyles();
          const spans = container.querySelectorAll('span');
          spans.forEach((el, i) => {
              el.style.animationDelay = (i * 30) + 'ms';
          });
      }, 200);
    });
}
