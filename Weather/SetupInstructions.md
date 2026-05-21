# Weather Forecast Dashboard - Setup Instructions

This guide explains how to set up and run the Weather Forecast Dashboard project locally.

## 1. Project Location

Open the project folder:

```bash
cd "F:\Dhruv's\Internship\pinnacle labs\Python Dev\code\PythonDev-PinnacleLabs\Weather"
```

The project structure should contain:

```plaintext
Weather/
|-- app.py
|-- requirements.txt
|-- README.md
|-- SetupInstructions.md
|-- .env
|-- templates/
|-- static/
|-- api/
|-- utils/
`-- database/
```

## 2. Required Software

Install the following before running the project:

- Python 3.10 or above
- pip
- Web browser such as Chrome, Edge, or Firefox
- Code editor such as VS Code

Check Python and pip:

```bash
python --version
pip --version
```

If `python` does not work, try:

```bash
py --version
```

## 3. Create a Virtual Environment

From inside the `Weather` folder, create a virtual environment:

```bash
python -m venv venv
```

If your system uses the Python launcher:

```bash
py -m venv venv
```

Activate the virtual environment on Windows PowerShell:

```bash
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```bash
.\venv\Scripts\Activate.ps1
```

After activation, the terminal should show `(venv)`.

## 4. Install Required Python Libraries

Install the required libraries:

```bash
pip install flask requests python-dotenv
```

Then save them into `requirements.txt`:

```bash
pip freeze > requirements.txt
```

For future setup, dependencies can be installed directly using:

```bash
pip install -r requirements.txt
```

## 5. Create API Accounts

The dashboard requires weather and news data from external APIs.

### OpenWeatherMap API

Used for:

- Current weather
- Hourly forecast
- Temperature data
- Rain or precipitation probability
- Weather condition codes

Setup steps:

1. Visit `https://openweathermap.org/api`
2. Create a free account.
3. Generate an API key.
4. Keep the key ready for the `.env` file.

### NewsAPI

Used for:

- Weather news
- Cyclone alerts
- Storm warnings
- Natural disaster reports

Setup steps:

1. Visit `https://newsapi.org/`
2. Create a free account.
3. Generate an API key.
4. Keep the key ready for the `.env` file.

## 6. Configure Environment Variables

Open the `.env` file and add:

```env
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=True

OPENWEATHER_API_KEY=your_openweathermap_api_key_here
NEWS_API_KEY=your_newsapi_key_here

DATABASE_PATH=database/search_history.db
DEFAULT_UNIT=metric
REFRESH_INTERVAL_MINUTES=15
```

Replace:

- `your_openweathermap_api_key_here` with your OpenWeatherMap API key
- `your_newsapi_key_here` with your NewsAPI key

Do not share the `.env` file publicly because it contains private API keys.

## 7. Database Setup

The project uses SQLite for optional local storage.

Database file:

```plaintext
database/search_history.db
```

It can be used to store:

- Search history
- Favorite locations
- User settings
- Theme preferences

If the database file is missing, create it manually:

```bash
type nul > database\search_history.db
```

The Flask app can later create tables automatically when database logic is implemented.

Suggested table for search history:

```sql
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 8. Recommended File Responsibilities

Use the files as follows:

```plaintext
app.py
Main Flask application and route definitions.

api/weather_api.py
OpenWeatherMap API request logic.

api/news_api.py
NewsAPI request logic.

utils/weather_mapper.py
Map API weather conditions to app themes and display labels.

utils/theme_manager.py
Handle dynamic weather theme selection.

utils/helpers.py
Common helper functions such as validation and formatting.

templates/index.html
Home page with manual city input and browser geolocation option.

templates/dashboard.html
Main weather dashboard page.

templates/weather_news.html
Weather alerts and news page.

static/css/style.css
Main layout and component styling.

static/css/themes.css
Weather-based theme styles.

static/css/animations.css
Weather animation styles.

static/js/main.js
Shared frontend logic.

static/js/weather.js
Weather fetch, location detection, refresh, and UI update logic.

static/js/charts.js
Hourly forecast and precipitation chart logic.

static/js/themes.js
Client-side theme switching logic.
```

## 9. Browser Geolocation Setup

The project can detect the user's location using:

```javascript
navigator.geolocation.getCurrentPosition()
```

Browser behavior:

- The browser asks permission to access location.
- If permission is allowed, latitude and longitude are captured.
- Weather data can then be loaded automatically.

Important notes:

- Geolocation works best on `localhost` or HTTPS.
- Users can deny permission, so manual city search should remain available.
- Always handle geolocation errors in JavaScript.

## 10. Suggested Flask Routes

Recommended page routes:

```plaintext
/                  Home page
/dashboard          Weather dashboard
/weather-news       Weather news page
```

Recommended API routes:

```plaintext
/api/weather/current
/api/weather/hourly
/api/weather/alerts
/api/weather/news
```

Example route purpose:

- `/api/weather/current` returns current weather for a city or coordinates.
- `/api/weather/hourly` returns hourly temperature and condition data.
- `/api/weather/alerts` returns severe weather alerts if available.
- `/api/weather/news` returns weather-related news from NewsAPI.

## 11. Run the Flask Application

Make sure the virtual environment is active:

```bash
.\venv\Scripts\Activate.ps1
```

Run the application:

```bash
python app.py
```

Or use Flask:

```bash
flask run
```

Open the browser at:

```plaintext
http://127.0.0.1:5000
```

## 12. Development Workflow

Follow this workflow while building the project:

1. Create the base Flask app in `app.py`.
2. Add HTML pages in the `templates` folder.
3. Add common styling in `static/css/style.css`.
4. Add weather themes in `static/css/themes.css`.
5. Add weather animations in `static/css/animations.css`.
6. Add OpenWeatherMap API logic in `api/weather_api.py`.
7. Add NewsAPI logic in `api/news_api.py`.
8. Add city search and geolocation logic in `static/js/weather.js`.
9. Add chart logic in `static/js/charts.js`.
10. Add theme switching logic in `static/js/themes.js`.
11. Store search history in `database/search_history.db`.
12. Test the dashboard with different cities and weather conditions.

## 13. Testing Checklist

Before submitting or presenting the project, verify:

- Home page loads correctly.
- Manual city search works.
- Browser geolocation permission appears.
- Weather data loads using OpenWeatherMap.
- News data loads using NewsAPI.
- Dashboard cards display temperature, weather condition, rain chance, and news.
- Temperature unit toggle works for Celsius and Fahrenheit.
- Dynamic themes change based on weather conditions.
- Weather animations display correctly.
- Search history is stored correctly if database logic is implemented.
- App handles invalid city names.
- App handles missing API keys.
- App handles API request failures.
- UI is responsive on mobile and desktop.

## 14. Common Problems and Fixes

### Virtual environment activation is blocked

Run:

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate:

```bash
.\venv\Scripts\Activate.ps1
```

### Flask command is not recognized

Install Flask:

```bash
pip install flask
```

Or run:

```bash
python app.py
```

### API data is not loading

Check:

- `.env` file exists.
- API keys are correct.
- `python-dotenv` is installed.
- Internet connection is working.
- API account is active.

### Location popup is not appearing

Check:

- Browser location permission is not blocked.
- App is running on `localhost`.
- JavaScript console does not show errors.

### Database errors

Check:

- `database` folder exists.
- `search_history.db` exists.
- Database path in `.env` is correct.

## 15. Final Expected Output

After setup, the project should run as a Flask-based Weather Forecast Dashboard with:

- Real-time weather monitoring
- Manual city search
- Browser location detection
- Dynamic weather themes
- Hourly temperature visualization
- Rain and precipitation forecast
- Weather news and alerts
- Search history support
- Responsive frontend design
