(function () {
  const chartInstances = {};

  function getThemeColor() {
    return getComputedStyle(document.documentElement).getPropertyValue("--theme-accent").trim() || "#67e8f9";
  }

  function baseOptions(title, chartOptions = {}) {
    return {
      responsive: true,
      maintainAspectRatio: chartOptions.maintainAspectRatio ?? true,
      resizeDelay: 120,
      layout: {
        padding: chartOptions.padding || {
          top: 10,
          right: 16,
          bottom: 10,
          left: 10
        }
      },
      plugins: {
        legend: {
          position: "top",
          labels: {
            color: "#f8fafc",
            boxWidth: 14,
            boxHeight: 14,
            padding: 18,
            font: {
              size: 13,
              weight: "700"
            }
          }
        },
        title: {
          display: Boolean(title),
          text: title,
          color: "#f8fafc",
          font: {
            size: chartOptions.titleSize || 16,
            weight: "900"
          },
          padding: {
            top: 4,
            bottom: 22
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: "rgba(248, 250, 252, 0.78)",
            padding: 10,
            maxRotation: 0,
            autoSkipPadding: 24,
            font: {
              size: chartOptions.tickSize || 12,
              weight: "700"
            }
          },
          grid: {
            color: "rgba(255, 255, 255, 0.08)"
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: "rgba(248, 250, 252, 0.78)",
            padding: 12,
            font: {
              size: chartOptions.tickSize || 12,
              weight: "700"
            }
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
            label: "Temperature (C)",
            data: hourly.map((item) => item.temperature),
            borderColor: accent,
            backgroundColor: "rgba(125, 211, 252, 0.18)",
            borderWidth: 3,
            fill: true,
            tension: 0.38,
            pointRadius: 5,
            pointHoverRadius: 8,
            pointBorderWidth: 2
          },
          {
            label: "Feels Like (C)",
            data: hourly.map((item) => item.feels_like),
            borderColor: "rgba(253, 224, 71, 0.95)",
            backgroundColor: "rgba(253, 224, 71, 0.12)",
            borderWidth: 3,
            fill: false,
            tension: 0.38,
            pointRadius: 4,
            pointHoverRadius: 7,
            pointBorderWidth: 2
          }
        ]
      },
      options: baseOptions("Temperature Trend", {
        maintainAspectRatio: false,
        titleSize: 18,
        tickSize: 13,
        padding: {
          top: 12,
          right: 28,
          bottom: 18,
          left: 16
        }
      })
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
    const options = baseOptions("Precipitation and Storm Risk");
    options.scales.y.max = 100;

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
      options
    });
  }

  window.WeatherCharts = {
    renderTemperatureChart,
    renderRainfallChart,
    renderPrecipitationChart
  };
})();
