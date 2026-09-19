import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Live Data Dashboard", layout="wide")
st.title("🌍 Live Data Dashboard")
st.markdown("Aggregating weather, markets, sports, and news from live public APIs.")

tab1, tab2, tab3, tab4 = st.tabs(["🌦️ Weather", "💰 Markets", "⚽ Sports", "📰 News"])

with tab1:
    st.subheader("Current Weather")

    city = st.text_input("Enter a city name", value="Lagos")

    if city:
        api_key = st.secrets["OPENWEATHER_API_KEY"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{data['main']['temp']}°C")
            col2.metric("Feels Like", f"{data['main']['feels_like']}°C")
            col3.metric("Humidity", f"{data['main']['humidity']}%")

            st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
            st.write(f"**Wind Speed:** {data['wind']['speed']} m/s")

        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                st.error("API key invalid or not yet activated. New OpenWeatherMap keys can take up to 2 hours to activate after signup.")
            elif response.status_code == 404:
                st.error(f"Could not find weather data for '{city}'. Check the spelling and try again.")
            else:
                st.error(f"Weather API error: {e}")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch weather data: {e}")

with tab2:
    st.subheader("Live Cryptocurrency Prices")

    coins = st.multiselect(
        "Select coins to track",
        options=["bitcoin", "ethereum", "solana", "cardano", "dogecoin"],
        default=["bitcoin", "ethereum", "solana"]
    )

    if coins:
        coin_ids = ",".join(coins)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_ids}&vs_currencies=usd&include_24hr_change=true"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            rows = []
            for coin, values in data.items():
                rows.append({
                    "Coin": coin.capitalize(),
                    "Price (USD)": f"${values['usd']:,.2f}",
                    "24h Change (%)": f"{values.get('usd_24h_change', 0):.2f}%"
                })

            df_prices = pd.DataFrame(rows)
            st.dataframe(df_prices, use_container_width=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch data: {e}")
    else:
        st.info("Select at least one coin above.")

with tab3:
    st.subheader("Recent Match Results")

    league_options = {
        "English Premier League": "4328",
        "Spanish La Liga": "4335",
        "UEFA Champions League": "4480",
        "NBA": "4387"
    }

    league_name = st.selectbox("Select a league", options=list(league_options.keys()))
    league_id = league_options[league_name]

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id={league_id}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        events = data.get('events')

        if events:
            rows = []
            for event in events[:10]:  # show 10 most recent
                rows.append({
                    "Date": event.get('dateEvent'),
                    "Home": event.get('strHomeTeam'),
                    "Score": f"{event.get('intHomeScore', '-')} - {event.get('intAwayScore', '-')}",
                    "Away": event.get('strAwayTeam')
                })
            df_matches = pd.DataFrame(rows)
            st.dataframe(df_matches, use_container_width=True)
        else:
            st.info(f"No recent match data available for {league_name}.")

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch sports data: {e}")

with tab4:
    st.subheader("Latest Headlines")

    topic = st.text_input("Search topic", value="technology")

    if topic:
        api_key = st.secrets["NEWS_API_KEY"]
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&apiKey={api_key}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            articles = data.get('articles', [])[:8]  # show top 8

            if articles:
                for article in articles:
                    st.markdown(f"**[{article['title']}]({article['url']})**")
                    st.caption(f"{article['source']['name']} • {article['publishedAt'][:10]}")
                    st.write("---")
            else:
                st.info(f"No articles found for '{topic}'.")

        except requests.exceptions.HTTPError:
            st.error("API key invalid or not yet activated, or rate limit reached.")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch news data: {e}")