import os
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
REQUEST_TIMEOUT = 10


class WeatherAPIError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _get_api_key():
    api_key = (
        os.getenv("OPENWEATHER_API_KEY")
        or os.getenv("OPENWEATHERMAP_API_KEY")
        or os.getenv("WEATHER_API_KEY")
    )

    if not api_key:
        raise WeatherAPIError("OpenWeatherMap API key is missing. Add it to the .env file.", 500)

    return api_key


def _request_weather(params):
    request_params = {
        **params,
        "appid": _get_api_key(),
        "units": os.getenv("DEFAULT_UNIT", "metric"),
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=request_params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout as exc:
        raise WeatherAPIError("Weather service request timed out. Please try again.", 504) from exc
    except requests.exceptions.ConnectionError as exc:
        raise WeatherAPIError("Unable to connect to the weather service. Check your internet connection.", 503) from exc
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError("Weather service request failed. Please try again.", 502) from exc

    if response.status_code == 401:
        raise WeatherAPIError("Invalid OpenWeatherMap API key.", 500)

    if response.status_code == 404:
        raise WeatherAPIError("City not found. Please enter a valid city name.", 404)

    if response.status_code == 429:
        raise WeatherAPIError("Weather API rate limit reached. Please try again later.", 429)

    if not response.ok:
        raise WeatherAPIError("Weather data is temporarily unavailable.", response.status_code)

    return _format_weather(response.json())


def _request_forecast(params):
    request_params = {
        **params,
        "appid": _get_api_key(),
        "units": os.getenv("DEFAULT_UNIT", "metric"),
    }

    try:
        response = requests.get(OPENWEATHER_FORECAST_URL, params=request_params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout as exc:
        raise WeatherAPIError("Forecast service request timed out. Please try again.", 504) from exc
    except requests.exceptions.ConnectionError as exc:
        raise WeatherAPIError("Unable to connect to the forecast service. Check your internet connection.", 503) from exc
    except requests.exceptions.RequestException as exc:
        raise WeatherAPIError("Forecast service request failed. Please try again.", 502) from exc

    if response.status_code == 401:
        raise WeatherAPIError("Invalid OpenWeatherMap API key.", 500)

    if response.status_code == 404:
        raise WeatherAPIError("Forecast location not found.", 404)

    if response.status_code == 429:
        raise WeatherAPIError("Weather API rate limit reached. Please try again later.", 429)

    if not response.ok:
        raise WeatherAPIError("Forecast data is temporarily unavailable.", response.status_code)

    return _format_forecast(response.json())


def _format_weather(data):
    main = data.get("main", {})
    weather_items = data.get("weather") or [{}]
    weather = weather_items[0]
    wind = data.get("wind", {})
    coord = data.get("coord", {})

    try:
        return {
            "city": data["name"],
            "temperature": round(float(main["temp"])),
            "feels_like": round(float(main["feels_like"])),
            "temp_min": round(float(main.get("temp_min", main["temp"]))),
            "temp_max": round(float(main.get("temp_max", main["temp"]))),
            "humidity": int(main["humidity"]),
            "pressure": int(main["pressure"]),
            "condition": weather.get("main", "Unknown"),
            "description": weather.get("description", "Weather details unavailable"),
            "icon": weather.get("icon", ""),
            "wind_speed": float(wind.get("speed", 0)),
            "coordinates": {
                "lat": float(coord.get("lat", 0)),
                "lon": float(coord.get("lon", 0)),
            },
        }
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherAPIError("Weather service returned incomplete data.", 502) from exc


def _format_forecast(data):
    city_data = data.get("city", {})
    forecast_items = data.get("list", [])[:12]
    hourly = []

    for item in forecast_items:
        main = item.get("main", {})
        weather_items = item.get("weather") or [{}]
        weather = weather_items[0]
        rain = item.get("rain", {})
        snow = item.get("snow", {})
        wind = item.get("wind", {})
        condition = weather.get("main", "Unknown")
        pop = float(item.get("pop", 0))
        rainfall = float(rain.get("3h", 0))
        snowfall = float(snow.get("3h", 0))
        thunderstorm_probability = round(pop * 100) if condition == "Thunderstorm" else 0

        hourly.append(
            {
                "time": item.get("dt_txt", ""),
                "label": _format_forecast_label(item.get("dt_txt", "")),
                "temperature": round(float(main.get("temp", 0))),
                "feels_like": round(float(main.get("feels_like", 0))),
                "humidity": int(main.get("humidity", 0)),
                "condition": condition,
                "description": weather.get("description", "Weather details unavailable"),
                "icon": weather.get("icon", ""),
                "rain_probability": round(pop * 100),
                "precipitation": round(pop * 100),
                "rainfall": rainfall + snowfall,
                "thunderstorm_probability": thunderstorm_probability,
                "wind_speed": float(wind.get("speed", 0)),
            }
        )

    if not hourly:
        raise WeatherAPIError("Forecast service returned no forecast items.", 502)

    return {
        "city": city_data.get("name", "Selected Location"),
        "country": city_data.get("country", ""),
        "hourly": hourly,
        "summary": {
            "rain_chance": max(item["rain_probability"] for item in hourly),
            "precipitation": max(item["precipitation"] for item in hourly),
            "thunderstorm_probability": max(item["thunderstorm_probability"] for item in hourly),
            "rainfall": round(sum(item["rainfall"] for item in hourly), 2),
        },
    }


def _format_forecast_label(dt_text):
    if not dt_text or " " not in dt_text:
        return dt_text

    hour = int(dt_text.split(" ")[1].split(":")[0])
    suffix = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour} {suffix}"


def _build_alerts_from_forecast(forecast):
    hourly = forecast["hourly"]
    alerts = []

    highest_rain = max(hourly, key=lambda item: item["rain_probability"])
    highest_storm = max(hourly, key=lambda item: item["thunderstorm_probability"])
    highest_wind = max(hourly, key=lambda item: item["wind_speed"])
    highest_temp = max(hourly, key=lambda item: item["temperature"])
    lowest_temp = min(hourly, key=lambda item: item["temperature"])

    if highest_storm["thunderstorm_probability"] >= 40:
        alerts.append(
            {
                "title": "Thunderstorm risk detected",
                "description": f"{highest_storm['thunderstorm_probability']}% thunderstorm probability around {highest_storm['label']}.",
                "severity": "High" if highest_storm["thunderstorm_probability"] >= 70 else "Medium",
                "time": highest_storm["time"],
            }
        )

    if highest_rain["rain_probability"] >= 55:
        alerts.append(
            {
                "title": "Rainfall warning",
                "description": f"{highest_rain['rain_probability']}% rain probability around {highest_rain['label']}.",
                "severity": "High" if highest_rain["rain_probability"] >= 75 else "Medium",
                "time": highest_rain["time"],
            }
        )

    if highest_wind["wind_speed"] >= 10:
        alerts.append(
            {
                "title": "High wind watch",
                "description": f"Wind speed may reach {highest_wind['wind_speed']:.1f} m/s around {highest_wind['label']}.",
                "severity": "Medium",
                "time": highest_wind["time"],
            }
        )

    if highest_temp["temperature"] >= 40:
        alerts.append(
            {
                "title": "Heat advisory",
                "description": f"Temperature may reach {highest_temp['temperature']}°C around {highest_temp['label']}.",
                "severity": "High",
                "time": highest_temp["time"],
            }
        )

    if lowest_temp["temperature"] <= 2:
        alerts.append(
            {
                "title": "Cold weather advisory",
                "description": f"Temperature may drop to {lowest_temp['temperature']}°C around {lowest_temp['label']}.",
                "severity": "Medium",
                "time": lowest_temp["time"],
            }
        )

    if not alerts:
        alerts.append(
            {
                "title": "No severe weather alerts detected",
                "description": "Forecast signals are currently within normal ranges for this location.",
                "severity": "Low",
                "time": hourly[0]["time"],
            }
        )

    return {"city": forecast["city"], "alerts": alerts}


def get_current_weather(city):
    normalized_city = city.strip()

    if not normalized_city:
        raise WeatherAPIError("City name is required.", 400)

    return _request_weather({"q": normalized_city})


def get_weather_by_coords(lat, lon):
    return _request_weather({"lat": lat, "lon": lon})


def get_hourly_forecast(city):
    normalized_city = city.strip()

    if not normalized_city:
        raise WeatherAPIError("City name is required.", 400)

    return _request_forecast({"q": normalized_city})


def get_hourly_forecast_by_coords(lat, lon):
    return _request_forecast({"lat": lat, "lon": lon})


def get_weather_alerts(city=None, lat=None, lon=None):
    if city:
        forecast = get_hourly_forecast(city)
    else:
        forecast = get_hourly_forecast_by_coords(lat, lon)

    return _build_alerts_from_forecast(forecast)
