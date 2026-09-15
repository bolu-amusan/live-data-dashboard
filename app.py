import streamlit as st

st.set_page_config(page_title="Live Data Dashboard", layout="wide")
st.title("🌍 Live Data Dashboard")
st.markdown("Aggregating weather, markets, sports, and news from live public APIs.")

tab1, tab2, tab3, tab4 = st.tabs(["🌦️ Weather", "💰 Markets", "⚽ Sports", "📰 News"])

with tab1:
    st.write("Weather content coming soon...")

with tab2:
    st.write("Markets content coming soon...")

with tab3:
    st.write("Sports content coming soon...")

with tab4:
    st.write("News content coming soon...")