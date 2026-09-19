# Live Data Dashboard

A multi-source dashboard aggregating real-time data from four independent public APIs — weather, cryptocurrency prices, sports results, and news headlines — built with Python and Streamlit.

🔗 **[View the live dashboard](https://live-data-dashboard-m2isxw4zwqbf4bkkxew4cb.streamlit.app/)**

## Overview
Unlike the earlier projects in this portfolio, which analyze static or periodically-updated datasets, this project works entirely with **live data** — every value shown is fetched fresh from an external API at the moment the page loads. This project demonstrates working with multiple third-party APIs with different authentication methods, response formats, and failure modes, unified into a single clean interface.

## Tech Stack
- Python (requests, pandas)
- Streamlit (multi-tab layout, secrets management)
- APIs: OpenWeatherMap, CoinGecko, TheSportsDB, NewsAPI

## Features

**🌦️ Weather** — current conditions for any city worldwide (temperature, feels-like, humidity, wind, condition)

**💰 Markets** — live cryptocurrency prices with 24-hour change, user-selectable coin list (CoinGecko — no API key required)

**⚽ Sports** — recent match results across selectable leagues (Premier League, La Liga, Champions League, NBA)

**📰 News** — latest headlines on any user-searched topic, with clickable links to full articles

## Key Technical Decisions

**1. Secrets management.** API keys are never hardcoded or committed to the repository. They're stored in `.streamlit/secrets.toml` locally (excluded via `.gitignore`) and configured separately in Streamlit Cloud's secrets manager for the deployed version.

**2. Defensive error handling.** Every API call is wrapped in try/except blocks that distinguish between different failure types (e.g., invalid/inactive API key vs. city not found vs. general network failure), so the app fails gracefully with a clear message rather than crashing.

**3. No-key-required starting point.** The Markets tab (CoinGecko) was built first since it requires no signup or authentication — this let the core "fetch → parse → display" pattern get validated quickly before adding the complexity of API key management for the other three tabs.

**4. Consistent pattern across tabs.** All four tabs follow the same structure (fetch, parse into a clean format, display, handle errors) despite each API having a completely different response shape — demonstrating the ability to normalize inconsistent external data into a consistent internal presentation.

## Setup / How to Run

**Easiest:** Visit the [live dashboard](https://live-data-dashboard-m2isxw4zwqbf4bkkxew4cb.streamlit.app/) — no setup required.

**To run locally:**
1. Clone this repo
2. Install dependencies: `pip install -r requirements.txt`
3. Get free API keys from [OpenWeatherMap](https://openweathermap.org/api) and [NewsAPI](https://newsapi.org/) (CoinGecko and TheSportsDB test tier need no key)
4. Create `.streamlit/secrets.toml`:
```toml
   OPENWEATHER_API_KEY = "type_in_your_key_here"
   NEWS_API_KEY = "type_in_your_key_here"
```
5. Run: `streamlit run app.py`

## Honest Limitations
- TheSportsDB is used via its free public test key, which is rate-limited and intended for development — a production version would use a paid tier or a more robust sports API
- NewsAPI's free tier has request limits and some restrictions on commercial use
- No caching is implemented — every tab interaction triggers a fresh API call, which is fine for a portfolio demo but would need rate-limit-aware caching (e.g., `st.cache_data` with a TTL) for heavier real-world use