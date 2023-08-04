import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
from pyowm.owm import OWM

API_KEY = "d03df81fa6320b1f7fbb33c667d4e3c6"
BASE_URL = "http://api.openweathermap.org/data/2.5"

owm = OWM(API_KEY)

def get_current_weather(city_name):
    endpoint = "/weather"
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()
    return data

def get_5_day_forecast(city_name):
    endpoint = "/forecast"
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL + endpoint, params=params)
    data = response.json()
    return data

def get_weather_icon(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}.png"

st.title("Weather App")

city_name = st.text_input("Enter city name:", "New York")
if st.button("Get Weather"):
    current_weather_data = get_current_weather(city_name)
    
    if current_weather_data["cod"] == 200:
        st.subheader("Current Weather")
        weather_description = current_weather_data['weather'][0]['description'].capitalize()
        temperature = current_weather_data['main']['temp']
        humidity = current_weather_data['main']['humidity']
        wind_speed = current_weather_data['wind']['speed']
        st.write(f"Weather: {weather_description}")
        st.write(f"Temperature: {temperature} °C")
        st.write(f"Humidity: {humidity}%")
        st.write(f"Wind Speed: {wind_speed} m/s")
        icon_code = current_weather_data['weather'][0]['icon']
        icon_url = get_weather_icon(icon_code)
        st.image(icon_url, caption=weather_description, width=100)
        
        st.subheader("5-Day Forecast")
        forecast_data = get_5_day_forecast(city_name)
        
        fig, axes = plt.subplots(1, 5, figsize=(20, 5))
        for i, entry in enumerate(forecast_data['list'][:5]):
            timestamp = entry['dt']
            date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            weather_description = entry['weather'][0]['description'].capitalize()
            temperature = entry['main']['temp']
            humidity = entry['main']['humidity']
            wind_speed = entry['wind']['speed']
            icon_code = entry['weather'][0]['icon']
            
            axes[i].set_title(date)
            axes[i].text(0.5, 0.6, f"Weather: {weather_description}\nTemp: {temperature} °C\nHumidity: {humidity}%\nWind: {wind_speed} m/s",
                          horizontalalignment='center', verticalalignment='center', transform=axes[i].transAxes)
            axes[i].imshow(Image.open(requests.get(get_weather_icon(icon_code), stream=True).raw))
            axes[i].axis('off')
        
        st.pyplot(fig)
    else:
        st.write("City not found. Please check the city name and try again.")
