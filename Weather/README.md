# Weather Forecast Dashboard

A Flask-based weather dashboard that shows live weather data, forecast charts, dynamic weather themes, and weather-related news.

## Current Working Features

- Manual city search from the home page
- Browser geolocation using `navigator.geolocation.getCurrentPosition()`
- Live current weather from OpenWeatherMap
- Weather lookup by city name
- Weather lookup by latitude and longitude
- Dashboard page that loads automatically after a successful search
- Responsive Bootstrap 5 UI
- Glassmorphism dashboard styling
- Dynamic weather-based themes
- Subtle weather animations
- Hourly forecast cards and charts
- Rain and precipitation forecast view
- Weather alerts derived from forecast data
- Weather news from NewsAPI
- Loading states and error messages

## Dashboard Cards

The dashboard currently includes four interactive cards.

### Current Temperature

Displays:

- Current temperature
- Feels-like temperature
- Maximum temperature
- Minimum temperature

On click:

- Opens a larger modal with a Chart.js temperature line graph
- Shows temperature and feels-like trends from forecast data

### Current Weather

Displays:

- Weather condition
- Weather description
- Weather icon
- Humidity
- Wind speed

On click:

- Opens a weather condition timeline
- Shows upcoming forecast conditions

### Rain / Precipitation

Displays:

- Rain chance
- Precipitation chance
- Thunderstorm probability

On click:

- Opens rainfall and precipitation charts
- Shows expected rainfall and storm probability

### Weather News

Displays:

- Weather-related news count
- Main alert or headline
- Severity label

On click:

- Opens a news and alerts modal
- Shows title, description, source, date, and severity

## Dynamic Themes

The dashboard changes theme automatically after weather data loads.

Currently supported themes:

- Sunny
- Semi-cloudy / haze / mist
- Rain
- Thunderstorm
- Snow

Theme changes include:

- Background gradients
- Accent colors
- Button colors
- Card highlight colors
- Weather animations

## Weather Animations

Current animations include:

- Sun glow for sunny weather
- Moving clouds for cloudy weather
- Rain streaks for rainy weather
- Lightning flash for thunderstorm weather
- Snowfall for snow weather

## APIs Used

### OpenWeatherMap

Used for:

- Current weather
- Temperature
- Feels-like temperature
- Humidity
- Pressure
- Wind speed
- Weather condition
- Weather icon
- Forecast data
- Rain and precipitation probability

### NewsAPI

Used for:

- Weather news
- Severe weather headlines
- Storm, rain, flood, and cyclone-related articles

## Flask Routes

### Page Routes

```text
/                  Home page
/dashboard          Weather dashboard
/weather-news       Redirects to dashboard
```

### API Routes

```text
/api/weather/current
/api/weather/location
/api/weather/hourly
/api/weather/alerts
/api/weather/news
```

## Project Structure

```text
Weather/
|-- app.py
|-- requirements.txt
|-- SetupInstructions.md
|-- README.md
|-- .env
|-- templates/
|   |-- index.html
|   |-- dashboard.html
|   `-- weather_news.html
|-- static/
|   |-- css/
|   |   |-- style.css
|   |   |-- themes.css
|   |   |-- dashboard.css
|   |   `-- animations.css
|   |-- js/
|   |   |-- main.js
|   |   |-- weather.js
|   |   |-- charts.js
|   |   `-- themes.js
|   |-- images/
|   `-- animations/
|-- api/
|   |-- weather_api.py
|   `-- news_api.py
|-- utils/
`-- database/
    `-- search_history.db
```

## Tech Stack

- Python
- Flask
- HTML5
- CSS3
- Bootstrap 5
- Vanilla JavaScript
- Chart.js
- OpenWeatherMap API
- NewsAPI
- python-dotenv
- requests

## Environment Variables

Create a `.env` file in the project root:

```env
WEATHER_API_KEY=your_openweathermap_api_key
NEWS_API_KEY=your_newsapi_key
SECRET_KEY=your_flask_secret_key
DEBUG=True
```

The app also supports these OpenWeatherMap key names:

```env
OPENWEATHER_API_KEY=your_openweathermap_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Notes

- Forecast data uses OpenWeatherMap forecast intervals, which are typically 3-hour forecast points.
- Weather alerts are generated from forecast conditions inside the app.
- SQLite files and utility folders exist in the structure, but database-backed features are not currently active.
