(function () {
  const chartInstances = {};

  function getThemeColor() {
    return getComputedStyle(document.documentElement).getPropertyValue("--theme-accent").trim() || "#67e8f9";
  }

  function baseOptions(title) {
    return {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          labels: {
            color: "#f8fafc",
            font: {
              weight: "700"
            }
          }
        },
        title: {
          display: Boolean(title),
          text: title,
          color: "#f8fafc",
          font: {
            size: 16,
            weight: "900"
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: "rgba(248, 250, 252, 0.78)"
          },
          grid: {
            color: "rgba(255, 255, 255, 0.08)"
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "rgba(248, 250, 252, 0.78)"
          },
          grid: {
            color: "rgba(255, 255, 255, 0.08)"
          }
        }
      }
    };
  }

  function renderChart(canvasId, config) {
    if (!window.Chart) {
      return;
    }

    const canvas = document.getElementById(canvasId);

    if (!canvas) {
      return;
    }

    if (chartInstances[canvasId]) {
      chartInstances[canvasId].destroy();
    }

    chartInstances[canvasId] = new Chart(canvas, config);
  }

  function renderTemperatureChart(hourly) {
    const accent = getThemeColor();

    renderChart("temperatureChart", {
      type: "line",
      data: {
        labels: hourly.map((item) => item.label),
        datasets: [
          {
            label: "Temperature °C",
            data: hourly.map((item) => item.temperature),
            borderColor: accent,
            backgroundColor: "rgba(125, 211, 252, 0.18)",
            fill: true,
            tension: 0.38,
            pointRadius: 4,
            pointHoverRadius: 6
          },
          {
            label: "Feels Like °C",
            data: hourly.map((item) => item.feels_like),
            borderColor: "rgba(253, 224, 71, 0.95)",
            backgroundColor: "rgba(253, 224, 71, 0.12)",
            fill: false,
            tension: 0.38,
            pointRadius: 3,
            pointHoverRadius: 5
          }
        ]
      },
      options: baseOptions("Temperature Trend")
    });
  }

  function renderRainfallChart(hourly) {
    renderChart("rainfallChart", {
      type: "bar",
      data: {
        labels: hourly.map((item) => item.label),
        datasets: [
          {
            label: "Rainfall mm",
            data: hourly.map((item) => item.rainfall),
            backgroundColor: "rgba(103, 232, 249, 0.62)",
            borderColor: "rgba(103, 232, 249, 1)",
            borderWidth: 1
          }
        ]
      },
      options: baseOptions("Expected Rainfall")
    });
  }

  function renderPrecipitationChart(hourly) {
    renderChart("precipitationChart", {
      type: "line",
      data: {
        labels: hourly.map((item) => item.label),
        datasets: [
          {
            label: "Precipitation %",
            data: hourly.map((item) => item.precipitation),
            borderColor: "rgba(96, 165, 250, 1)",
            backgroundColor: "rgba(96, 165, 250, 0.16)",
            fill: true,
            tension: 0.35
          },
          {
            label: "Storm %",
            data: hourly.map((item) => item.thunderstorm_probability),
            borderColor: "rgba(248, 113, 113, 1)",
            backgroundColor: "rgba(248, 113, 113, 0.12)",
            fill: false,
            tension: 0.35
          }
        ]
      },
      options: {
        ...baseOptions("Precipitation and Storm Risk"),
        scales: {
          ...baseOptions().scales,
          y: {
            ...baseOptions().scales.y,
            max: 100
          }
        }
      }
    });
  }

  window.WeatherCharts = {
    renderTemperatureChart,
    renderRainfallChart,
    renderPrecipitationChart
  };
})();
