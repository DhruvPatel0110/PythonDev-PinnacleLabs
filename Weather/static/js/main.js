const weatherForm = document.querySelector("#weatherForm");
const cityInput = document.querySelector("#cityInput");
const locationButton = document.querySelector("#locationButton");
const submitButton = weatherForm.querySelector("button[type='submit']");
const statusPanel = document.querySelector("#statusPanel");
const alertPanel = document.querySelector("#alertPanel");
const weatherResult = document.querySelector("#weatherResult");
const weatherCity = document.querySelector("#weatherCity");
const weatherTemperature = document.querySelector("#weatherTemperature");
const weatherFeelsLike = document.querySelector("#weatherFeelsLike");
const weatherHumidity = document.querySelector("#weatherHumidity");
const weatherPressure = document.querySelector("#weatherPressure");
const weatherCondition = document.querySelector("#weatherCondition");
const weatherDescription = document.querySelector("#weatherDescription");
const weatherIcon = document.querySelector("#weatherIcon");
const weatherWindSpeed = document.querySelector("#weatherWindSpeed");

const defaultSubmitText = submitButton.textContent;
const defaultLocationText = locationButton.textContent;

function setStatus(message, type = "neutral") {
  statusPanel.textContent = message;
  statusPanel.classList.remove("is-success", "is-warning", "is-error");

  if (type === "success") {
    statusPanel.classList.add("is-success");
  }

  if (type === "warning") {
    statusPanel.classList.add("is-warning");
  }

  if (type === "error") {
    statusPanel.classList.add("is-error");
  }
}

function normalizeCityName(value) {
  return value.trim().replace(/\s+/g, " ");
}

function showAlert(message) {
  alertPanel.textContent = message;
  alertPanel.classList.remove("d-none");
}

function hideAlert() {
  alertPanel.textContent = "";
  alertPanel.classList.add("d-none");
}

function setLoading(isLoading, activeButton) {
  submitButton.disabled = isLoading;
  locationButton.disabled = isLoading;

  if (!isLoading) {
    submitButton.textContent = defaultSubmitText;
    locationButton.textContent = defaultLocationText;
    return;
  }

  const loadingMarkup = '<span class="spinner-border spinner-border-sm me-2" aria-hidden="true"></span>Loading';

  if (activeButton === submitButton) {
    submitButton.innerHTML = loadingMarkup;
  }

  if (activeButton === locationButton) {
    locationButton.innerHTML = loadingMarkup;
  }
}

function formatWindSpeed(value) {
  return Number(value).toFixed(1);
}

function renderWeather(data) {
  weatherCity.textContent = data.city;
  weatherTemperature.textContent = data.temperature;
  weatherFeelsLike.textContent = data.feels_like;
  weatherHumidity.textContent = data.humidity;
  weatherPressure.textContent = data.pressure;
  weatherCondition.textContent = data.condition;
  weatherDescription.textContent = data.description;
  weatherWindSpeed.textContent = formatWindSpeed(data.wind_speed);
  weatherIcon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
  weatherIcon.alt = `${data.description} weather icon`;
  weatherResult.classList.remove("d-none");
}

function openDashboard(query) {
  try {
    sessionStorage.setItem("weatherDashboardQuery", JSON.stringify(query));
  } catch (error) {
    console.warn("Unable to store dashboard query:", error);
  }

  const params = new URLSearchParams();

  if (query.city) {
    params.set("city", query.city);
  } else {
    params.set("lat", query.lat);
    params.set("lon", query.lon);
  }

  window.location.href = `/dashboard?${params.toString()}`;
}

async function fetchWeather(url, activeButton, dashboardQuery) {
  hideAlert();
  setLoading(true, activeButton);
  setStatus("Fetching live weather data.", "warning");

  try {
    const response = await fetch(url, {
      headers: {
        "Accept": "application/json"
      }
    });
    let data = {};

    try {
      data = await response.json();
    } catch (parseError) {
      console.warn("Weather response was not valid JSON:", parseError);
    }

    if (!response.ok) {
      throw new Error(data.error || "Unable to fetch weather data.");
    }

    renderWeather(data);
    setStatus(`Live weather loaded for ${data.city}.`, "success");
    openDashboard(dashboardQuery || { city: data.city });
  } catch (error) {
    const message = error instanceof TypeError
      ? "No internet connection or weather service unavailable."
      : error.message || "No internet connection or weather service unavailable.";
    console.error("Weather fetch error:", error);
    showAlert(message);
    setStatus(message, "error");
  } finally {
    setLoading(false, activeButton);
  }
}

weatherForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const city = normalizeCityName(cityInput.value);

  if (!city) {
    const message = "Please enter a city name.";
    showAlert(message);
    setStatus(message, "warning");
    cityInput.focus();
    return;
  }

  console.log("Manual city selected:", city);
  const url = `/api/weather/current?city=${encodeURIComponent(city)}`;
  await fetchWeather(url, submitButton, { city });
});

locationButton.addEventListener("click", () => {
  hideAlert();

  if (!("geolocation" in navigator)) {
    setStatus("Geolocation is not supported by this browser.", "error");
    alert("Geolocation is not supported by this browser.");
    return;
  }

  setStatus("Requesting location permission.", "warning");
  setLoading(true, locationButton);

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const { latitude, longitude } = position.coords;
      console.log("Latitude:", latitude);
      console.log("Longitude:", longitude);
      console.log("Coordinates:", { latitude, longitude });

      const params = new URLSearchParams({
        lat: latitude,
        lon: longitude
      });
      await fetchWeather(`/api/weather/location?${params.toString()}`, locationButton, {
        lat: String(latitude),
        lon: String(longitude)
      });
    },
    (error) => {
      let message = "Unable to access your location.";

      if (error.code === error.PERMISSION_DENIED) {
        message = "Location permission was denied.";
      }

      if (error.code === error.POSITION_UNAVAILABLE) {
        message = "Location information is unavailable.";
      }

      if (error.code === error.TIMEOUT) {
        message = "Location request timed out.";
      }

      console.warn("Geolocation error:", error);
      showAlert(message);
      setStatus(message, "error");
      alert(message);
      setLoading(false, locationButton);
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    }
  );
});
