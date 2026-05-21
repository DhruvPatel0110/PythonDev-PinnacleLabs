(function () {
  const state = {
    query: null,
    current: null,
    forecast: null,
    alerts: null,
    news: null
  };

  const elements = {
    title: document.querySelector("#dashboardTitle"),
    subtitle: document.querySelector("#dashboardSubtitle"),
    alert: document.querySelector("#dashboardAlert"),
    searchForm: document.querySelector("#dashboardSearchForm"),
    cityInput: document.querySelector("#dashboardCityInput"),
    overviewIcon: document.querySelector("#overviewIcon"),
    overviewCondition: document.querySelector("#overviewCondition"),
    overviewTemperature: document.querySelector("#overviewTemperature"),
    overviewUpdated: document.querySelector("#overviewUpdated"),
    cardTemperature: document.querySelector("#cardTemperature"),
    cardFeelsLike: document.querySelector("#cardFeelsLike"),
    cardTempMax: document.querySelector("#cardTempMax"),
    cardTempMin: document.querySelector("#cardTempMin"),
    cardWeatherIcon: document.querySelector("#cardWeatherIcon"),
    cardCondition: document.querySelector("#cardCondition"),
    cardDescription: document.querySelector("#cardDescription"),
    cardHumidity: document.querySelector("#cardHumidity"),
    cardWind: document.querySelector("#cardWind"),
    cardRainChance: document.querySelector("#cardRainChance"),
    cardPrecipitation: document.querySelector("#cardPrecipitation"),
    cardStormChance: document.querySelector("#cardStormChance"),
    cardNewsCount: document.querySelector("#cardNewsCount"),
    cardNewsHeadline: document.querySelector("#cardNewsHeadline"),
    cardNewsSeverity: document.querySelector("#cardNewsSeverity"),
    conditionTimeline: document.querySelector("#conditionTimeline"),
    newsList: document.querySelector("#newsList")
  };

  function normalizeCityName(value) {
    return value.trim().replace(/\s+/g, " ");
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function showAlert(message) {
    elements.alert.textContent = message;
    elements.alert.classList.remove("d-none");
  }

  function hideAlert() {
    elements.alert.textContent = "";
    elements.alert.classList.add("d-none");
  }

  function getStoredQuery() {
    try {
      const stored = sessionStorage.getItem("weatherDashboardQuery");
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.warn("Could not read stored dashboard query:", error);
      return null;
    }
  }

  function storeQuery(query) {
    try {
      sessionStorage.setItem("weatherDashboardQuery", JSON.stringify(query));
    } catch (error) {
      console.warn("Could not store dashboard query:", error);
    }
  }

  function getInitialQuery() {
    const params = new URLSearchParams(window.location.search);
    const city = normalizeCityName(params.get("city") || "");
    const lat = params.get("lat");
    const lon = params.get("lon");

    if (city) {
      return { city };
    }

    if (lat && lon) {
      return { lat, lon };
    }

    return getStoredQuery() || { city: "Hyderabad" };
  }

  function buildParams(query) {
    const params = new URLSearchParams();

    if (query.city) {
      params.set("city", query.city);
    } else {
      params.set("lat", query.lat);
      params.set("lon", query.lon);
    }

    return params;
  }

  function currentWeatherUrl(query) {
    if (query.city) {
      return `/api/weather/current?city=${encodeURIComponent(query.city)}`;
    }

    const params = buildParams(query);
    return `/api/weather/location?${params.toString()}`;
  }

  function endpointUrl(path, query) {
    return `${path}?${buildParams(query).toString()}`;
  }

  async function fetchJson(url) {
    const response = await fetch(url, {
      headers: {
        "Accept": "application/json"
      }
    });
    let data = {};

    try {
      data = await response.json();
    } catch (error) {
      console.warn("Response was not valid JSON:", error);
    }

    if (!response.ok) {
      throw new Error(data.error || "Request failed.");
    }

    return data;
  }

  function setLoadingState() {
    hideAlert();
    elements.title.textContent = "Dashboard";
    elements.subtitle.textContent = "Loading live weather intelligence.";
    elements.overviewUpdated.textContent = "Fetching latest data";
    elements.cardNewsHeadline.textContent = "Loading severe weather news";
  }

  function setCurrentWeather(data) {
    const description = data.description || "weather details unavailable";
    const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;

    state.current = data;
    elements.title.textContent = data.city;
    elements.subtitle.textContent = `${description.charAt(0).toUpperCase()}${description.slice(1)} with ${data.humidity}% humidity and ${Number(data.wind_speed).toFixed(1)} m/s wind.`;
    elements.overviewIcon.src = iconUrl;
    elements.overviewIcon.alt = `${description} icon`;
    elements.overviewCondition.textContent = `${data.condition} / ${description}`;
    elements.overviewTemperature.textContent = data.temperature;
    elements.overviewUpdated.textContent = `Updated ${new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
    elements.cardTemperature.textContent = data.temperature;
    elements.cardFeelsLike.textContent = data.feels_like;
    elements.cardTempMax.textContent = data.temp_max;
    elements.cardTempMin.textContent = data.temp_min;
    elements.cardWeatherIcon.src = iconUrl;
    elements.cardWeatherIcon.alt = `${description} icon`;
    elements.cardCondition.textContent = data.condition;
    elements.cardDescription.textContent = description;
    elements.cardHumidity.textContent = data.humidity;
    elements.cardWind.textContent = Number(data.wind_speed).toFixed(1);

    if (window.WeatherTheme) {
      window.WeatherTheme.applyWeatherTheme(data.condition, description);
    }
  }

  function setForecast(data) {
    state.forecast = data;
    elements.cardRainChance.textContent = data.summary.rain_chance;
    elements.cardPrecipitation.textContent = data.summary.precipitation;
    elements.cardStormChance.textContent = data.summary.thunderstorm_probability;
    renderConditionTimeline(data.hourly);
  }

  function renderConditionTimeline(hourly) {
    elements.conditionTimeline.innerHTML = hourly
      .map((item) => {
        const iconUrl = `https://openweathermap.org/img/wn/${item.icon}.png`;
        return `
          <article class="timeline-item">
            <span class="timeline-time">${escapeHtml(item.label)}</span>
            <img src="${iconUrl}" alt="${escapeHtml(item.description)} icon">
            <div>
              <h3 class="timeline-condition">${escapeHtml(item.condition)}</h3>
              <p class="timeline-description text-capitalize">${escapeHtml(item.description)}</p>
            </div>
            <strong>${escapeHtml(item.temperature)}°C</strong>
          </article>
        `;
      })
      .join("");
  }

  function severityClass(severity) {
    return `severity-${String(severity || "Low").toLowerCase()}`;
  }

  function setNewsAndAlerts(alertsData, newsData) {
    state.alerts = alertsData;
    state.news = newsData;

    const alerts = alertsData.alerts || [];
    const articles = newsData.articles || [];
    const firstArticle = articles[0];
    const firstAlert = alerts[0];
    const highestSeverity = [...alerts, ...articles].find((item) => item.severity === "High")
      || [...alerts, ...articles].find((item) => item.severity === "Medium")
      || firstAlert
      || firstArticle;

    elements.cardNewsCount.textContent = String(alerts.length + articles.length);
    elements.cardNewsHeadline.textContent = firstAlert?.title || firstArticle?.title || "No severe weather news found";
    elements.cardNewsSeverity.textContent = `${highestSeverity?.severity || "Low"} severity`;
    elements.cardNewsSeverity.className = `news-severity-pill severity ${severityClass(highestSeverity?.severity)}`;
    renderNewsList(alerts, articles);
  }

  function renderNewsList(alerts, articles) {
    const alertHtml = alerts
      .map((alert) => `
        <article class="news-item">
          <span class="severity ${severityClass(alert.severity)}">${escapeHtml(alert.severity)} Alert</span>
          <h3>${escapeHtml(alert.title)}</h3>
          <p>${escapeHtml(alert.description)}</p>
          <span class="news-meta">${escapeHtml(alert.time || "Forecast based alert")}</span>
        </article>
      `)
      .join("");

    const newsHtml = articles
      .map((article) => `
        <article class="news-item">
          <span class="severity ${severityClass(article.severity)}">${escapeHtml(article.severity)} News</span>
          <h3>${escapeHtml(article.title)}</h3>
          <p>${escapeHtml(article.description)}</p>
          <span class="news-meta">${escapeHtml(article.source)} / ${escapeHtml(article.date)}</span>
          ${article.url ? `<a class="news-link" href="${escapeHtml(article.url)}" target="_blank" rel="noreferrer">Read full story</a>` : ""}
        </article>
      `)
      .join("");

    elements.newsList.innerHTML = alertHtml + newsHtml || `
      <article class="news-item">
        <span class="severity severity-low">Low News</span>
        <h3>No severe weather news found</h3>
        <p>NewsAPI did not return severe weather stories for this search right now.</p>
        <span class="news-meta">Live news check completed</span>
      </article>
    `;
  }

  async function loadNewsAndAlerts(query, current) {
    const newsParams = new URLSearchParams({
      city: current.city,
      condition: current.condition
    });

    try {
      const [alertsData, newsData] = await Promise.all([
        fetchJson(endpointUrl("/api/weather/alerts", query)),
        fetchJson(`/api/weather/news?${newsParams.toString()}`)
      ]);
      setNewsAndAlerts(alertsData, newsData);
    } catch (error) {
      console.error("News or alerts loading failed:", error);
      const fallbackAlerts = {
        alerts: [
          {
            title: "Weather news unavailable",
            description: error.message,
            severity: "Medium",
            time: new Date().toLocaleString()
          }
        ]
      };
      setNewsAndAlerts(fallbackAlerts, { articles: [] });
    }
  }

  async function loadDashboard(query) {
    state.query = query;
    storeQuery(query);
    setLoadingState();

    try {
      const [current, forecast] = await Promise.all([
        fetchJson(currentWeatherUrl(query)),
        fetchJson(endpointUrl("/api/weather/hourly", query))
      ]);

      setCurrentWeather(current);
      setForecast(forecast);
      await loadNewsAndAlerts(query, current);
    } catch (error) {
      const message = error instanceof TypeError
        ? "No internet connection or weather service unavailable."
        : error.message || "Unable to load dashboard weather data.";
      console.error("Dashboard loading failed:", error);
      showAlert(message);
      elements.subtitle.textContent = message;
    }
  }

  function handleDashboardSearch(event) {
    event.preventDefault();
    const city = normalizeCityName(elements.cityInput.value);

    if (!city) {
      showAlert("Please enter a city name.");
      elements.cityInput.focus();
      return;
    }

    const query = { city };
    const params = buildParams(query);
    history.pushState(query, "", `/dashboard?${params.toString()}`);
    loadDashboard(query);
    elements.cityInput.value = "";
  }

  function renderChartsForModal(modalId) {
    if (!state.forecast || !window.WeatherCharts) {
      return;
    }

    if (modalId === "temperatureModal") {
      window.WeatherCharts.renderTemperatureChart(state.forecast.hourly);
    }

    if (modalId === "rainModal") {
      window.WeatherCharts.renderRainfallChart(state.forecast.hourly);
      window.WeatherCharts.renderPrecipitationChart(state.forecast.hourly);
    }
  }

  elements.searchForm.addEventListener("submit", handleDashboardSearch);

  ["temperatureModal", "rainModal"].forEach((modalId) => {
    const modal = document.getElementById(modalId);
    modal.addEventListener("shown.bs.modal", () => renderChartsForModal(modalId));
  });

  window.addEventListener("popstate", () => {
    loadDashboard(getInitialQuery());
  });

  loadDashboard(getInitialQuery());
})();
