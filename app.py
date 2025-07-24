#hello this is deep


import streamlit as st
import requests
import plotly.graph_objs as go
from datetime import datetime

# OpenWeatherMap API Key
API_KEY = "8b6e20f6b65154029cbcbb5708a88149"

# Helper functions
def get_weather_data(city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(base_url, params=params)
    return response.json()

def get_forecast_data(city, units="metric"):
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": API_KEY, "units": units}
    response = requests.get(url, params=params)
    return response.json()

def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

def get_weather_icon(weather_main):
    icons = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Snow": "❄️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Mist": "🌫️"
    }
    return icons.get(weather_main, "🌍")

# Streamlit UI
st.title("🌤️ Real-Time Weather App")
city = st.text_input("Enter city name", "Chennai")

unit_toggle = st.radio("Select temperature unit", ("Celsius", "Fahrenheit"))
unit = "metric" if unit_toggle == "Celsius" else "imperial"
unit_symbol = "°C" if unit_toggle == "Celsius" else "°F"

if city:
    data = get_weather_data(city, unit)

    if data.get("cod") == 200:
        st.subheader(f"Weather in {data['name']}, {data['sys']['country']} {get_weather_icon(data['weather'][0]['main'])}")
        st.write(f"**Temperature:** {data['main']['temp']} {unit_symbol}")
        st.write(f"**Humidity:** {data['main']['humidity']}%")
        st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone']).strftime('%H:%M:%S')
        sunset = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone']).strftime('%H:%M:%S')
        st.write(f"**Sunrise:** {sunrise}")
        st.write(f"**Sunset:** {sunset}")

        # Forecast
        forecast = get_forecast_data(city, unit)
        st.subheader("5-Day Forecast")

        dates = []
        temps = []

        for item in forecast["list"]:
            time = datetime.fromtimestamp(item["dt"])
            if time.hour == 12:  # Midday only
                dates.append(time.strftime("%a %d"))
                temps.append(item["main"]["temp"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=temps, mode='lines+markers', name='Temp'))
        fig.update_layout(title="5-Day Temperature Forecast", xaxis_title="Date", yaxis_title=f"Temp ({unit_symbol})")
        st.plotly_chart(fig)
    else:
        st.error("City not found!")
