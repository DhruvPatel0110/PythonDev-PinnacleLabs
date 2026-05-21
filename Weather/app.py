import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from api.news_api import NewsAPIError, get_weather_news
from api.weather_api import (
    WeatherAPIError,
    get_current_weather,
    get_hourly_forecast,
    get_hourly_forecast_by_coords,
    get_weather_alerts,
    get_weather_by_coords,
)


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "weather-dashboard-dev-key")


@app.route("/")
def home():
    return render_template("index.html", app_name="Weather Forecast Dashboard")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", app_name="Weather Forecast Dashboard")


@app.route("/weather-news")
def weather_news():
    return render_template("weather_news.html", app_name="Weather News")


@app.get("/api/weather/current")
def current_weather():
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "City name is required."}), 400

    if len(city) > 80:
        return jsonify({"error": "City name is too long."}), 400

    try:
        return jsonify(get_current_weather(city))
    except WeatherAPIError as exc:
        return jsonify({"error": exc.message}), exc.status_code


def _get_location_query():
    city = request.args.get("city", "").strip()
    lat_value = request.args.get("lat", "").strip()
    lon_value = request.args.get("lon", "").strip()

    if city:
        if len(city) > 80:
            return None, jsonify({"error": "City name is too long."}), 400

        return {"city": city}, None, None

    if not lat_value or not lon_value:
        return None, jsonify({"error": "City or latitude and longitude are required."}), 400

    try:
        lat = float(lat_value)
        lon = float(lon_value)
    except ValueError:
        return None, jsonify({"error": "Latitude and longitude must be valid numbers."}), 400

    if not -90 <= lat <= 90:
        return None, jsonify({"error": "Latitude must be between -90 and 90."}), 400

    if not -180 <= lon <= 180:
        return None, jsonify({"error": "Longitude must be between -180 and 180."}), 400

    return {"lat": lat, "lon": lon}, None, None


@app.get("/api/weather/location")
def location_weather():
    lat_value = request.args.get("lat", "").strip()
    lon_value = request.args.get("lon", "").strip()

    if not lat_value or not lon_value:
        return jsonify({"error": "Latitude and longitude are required."}), 400

    try:
        lat = float(lat_value)
        lon = float(lon_value)
    except ValueError:
        return jsonify({"error": "Latitude and longitude must be valid numbers."}), 400

    if not -90 <= lat <= 90:
        return jsonify({"error": "Latitude must be between -90 and 90."}), 400

    if not -180 <= lon <= 180:
        return jsonify({"error": "Longitude must be between -180 and 180."}), 400

    try:
        return jsonify(get_weather_by_coords(lat, lon))
    except WeatherAPIError as exc:
        return jsonify({"error": exc.message}), exc.status_code


@app.get("/api/weather/hourly")
def hourly_forecast():
    location, error_response, status = _get_location_query()

    if error_response:
        return error_response, status

    try:
        if "city" in location:
            return jsonify(get_hourly_forecast(location["city"]))

        return jsonify(get_hourly_forecast_by_coords(location["lat"], location["lon"]))
    except WeatherAPIError as exc:
        return jsonify({"error": exc.message}), exc.status_code


@app.get("/api/weather/alerts")
def weather_alerts():
    location, error_response, status = _get_location_query()

    if error_response:
        return error_response, status

    try:
        if "city" in location:
            return jsonify(get_weather_alerts(city=location["city"]))

        return jsonify(get_weather_alerts(lat=location["lat"], lon=location["lon"]))
    except WeatherAPIError as exc:
        return jsonify({"error": exc.message}), exc.status_code


@app.get("/api/weather/news")
def weather_news_api():
    city = request.args.get("city", "").strip()
    condition = request.args.get("condition", "").strip()

    try:
        return jsonify(get_weather_news(city=city or None, condition=condition or None))
    except NewsAPIError as exc:
        return jsonify({"error": exc.message}), exc.status_code


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
