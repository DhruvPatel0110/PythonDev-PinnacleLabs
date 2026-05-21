import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

NEWS_API_URL = "https://newsapi.org/v2/everything"
REQUEST_TIMEOUT = 10


class NewsAPIError(Exception):
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _get_api_key():
    api_key = os.getenv("NEWS_API_KEY") or os.getenv("NEWSAPI_KEY")

    if not api_key:
        raise NewsAPIError("NewsAPI key is missing. Add NEWS_API_KEY to the .env file.", 500)

    return api_key


def _classify_severity(title, description):
    text = f"{title} {description}".lower()
    high_keywords = ("cyclone", "hurricane", "tornado", "red alert", "evacuation", "severe warning")
    medium_keywords = ("thunderstorm", "heavy rain", "flood", "storm", "landslide", "yellow alert")

    if any(keyword in text for keyword in high_keywords):
        return "High"

    if any(keyword in text for keyword in medium_keywords):
        return "Medium"

    return "Low"


def _format_date(value):
    if not value:
        return ""

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value

    return parsed.astimezone(timezone.utc).strftime("%d %b %Y, %I:%M %p UTC")


def get_weather_news(city=None, condition=None):
    severe_terms = [
        "severe weather",
        "cyclone",
        "storm",
        "rainfall",
        "thunderstorm",
        "flood",
        "weather warning",
        "red alert",
        "yellow alert",
    ]
    if city:
        location_terms = [city, "India"]
        location_query = " OR ".join(f'"{term}"' for term in location_terms)
        condition_query = " OR ".join(f'"{term}"' for term in severe_terms)
        query = f"({location_query}) AND ({condition_query})"
    else:
        query = " OR ".join(f'"{term}"' for term in severe_terms)

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 8,
        "apiKey": _get_api_key(),
    }

    try:
        response = requests.get(NEWS_API_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout as exc:
        raise NewsAPIError("News service request timed out. Please try again.", 504) from exc
    except requests.exceptions.ConnectionError as exc:
        raise NewsAPIError("Unable to connect to NewsAPI. Check your internet connection.", 503) from exc
    except requests.exceptions.RequestException as exc:
        raise NewsAPIError("News service request failed. Please try again.", 502) from exc

    if response.status_code == 401:
        raise NewsAPIError("Invalid NewsAPI key.", 500)

    if response.status_code == 429:
        raise NewsAPIError("NewsAPI rate limit reached. Please try again later.", 429)

    if not response.ok:
        raise NewsAPIError("Weather news is temporarily unavailable.", response.status_code)

    payload = response.json()
    articles = payload.get("articles", [])
    news_items = []

    for article in articles:
        title = article.get("title") or "Weather update"
        description = article.get("description") or "No description provided by the source."
        source = article.get("source", {}).get("name") or "NewsAPI"

        news_items.append(
            {
                "title": title,
                "description": description,
                "source": source,
                "date": _format_date(article.get("publishedAt")),
                "url": article.get("url", ""),
                "severity": _classify_severity(title, description),
            }
        )

    return {"city": city or "Global", "articles": news_items}
