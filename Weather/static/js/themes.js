(function () {
  const themeClasses = [
    "theme-sunny",
    "theme-cloudy",
    "theme-rain",
    "theme-thunderstorm",
    "theme-snow"
  ];

  function resolveTheme(condition = "", description = "") {
    const conditionText = condition.toLowerCase();
    const descriptionText = description.toLowerCase();
    const combined = `${conditionText} ${descriptionText}`;

    if (conditionText.includes("thunderstorm") || combined.includes("extreme") || combined.includes("overcast")) {
      return "theme-thunderstorm";
    }

    if (conditionText.includes("rain") || conditionText.includes("drizzle")) {
      return "theme-rain";
    }

    if (conditionText.includes("snow")) {
      return "theme-snow";
    }

    if (conditionText.includes("clear") || descriptionText.includes("sunny")) {
      return "theme-sunny";
    }

    if (
      conditionText.includes("cloud") ||
      conditionText.includes("mist") ||
      conditionText.includes("haze") ||
      conditionText.includes("fog")
    ) {
      return "theme-cloudy";
    }

    return "theme-cloudy";
  }

  function applyWeatherTheme(condition, description) {
    const theme = resolveTheme(condition, description);
    document.body.classList.remove(...themeClasses);
    document.body.classList.add(theme);
    document.body.dataset.weatherTheme = theme.replace("theme-", "");
    return theme;
  }

  window.WeatherTheme = {
    applyWeatherTheme,
    resolveTheme
  };
})();
