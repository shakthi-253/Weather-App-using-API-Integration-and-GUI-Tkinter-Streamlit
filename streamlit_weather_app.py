streamlit_weather_app.py
#!/usr/bin/env python3
"""
Weather App with Streamlit
A modern web-based weather application with an interactive interface
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
from io import BytesIO


class StreamlitWeatherApp:
    def _init_(self):
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0/direct"
        
    def setup_page(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Weather App",
            page_icon="🌤",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .weather-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin: 1rem 0;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
            margin: 0.5rem 0;
        }
        .forecast-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
            margin: 0.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Render the main header"""
        st.markdown('<h1 class="main-header">🌤 Weather App</h1>', unsafe_allow_html=True)
        st.markdown("---")
    
    def render_search_section(self):
        """Render the search section"""
        st.sidebar.header("🔍 Search Weather")
        
        # City input
        city = st.sidebar.text_input("Enter city name:", value="London", placeholder="e.g., London, New York")
        
        # Country code (optional)
        country = st.sidebar.text_input("Country code (optional):", placeholder="e.g., GB, US")
        
        # Search button
        search_button = st.sidebar.button("🌍 Get Weather", type="primary")
        
        return city, country, search_button
    
    def render_sidebar_info(self):
        """Render additional information in sidebar"""
        st.sidebar.markdown("---")
        st.sidebar.header("ℹ Information")
        st.sidebar.info("""
        This app provides:
        - Current weather conditions
        - 5-day weather forecast
        - Interactive weather charts
        - Detailed weather metrics
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.header("🔧 Settings")
        units = st.sidebar.selectbox("Temperature units:", ["Celsius", "Fahrenheit"])
        show_forecast = st.sidebar.checkbox("Show 5-day forecast", value=True)
        show_charts = st.sidebar.checkbox("Show weather charts", value=True)
        
        return units, show_forecast, show_charts
    
    def get_weather_data(self, city, country=""):
        """Fetch current weather data"""
        try:
            # Construct query
            query = f"{city},{country}" if country else city
            url = f"{self.base_url}?q={query}&appid={self.api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                st.error(f"Error: {data.get('message', 'Unknown error')}")
                return None
                
        except requests.RequestException as e:
            st.error(f"Network error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def get_forecast_data(self, city, country=""):
        """Fetch 5-day forecast data"""
        try:
            query = f"{city},{country}" if country else city
            url = f"{self.forecast_url}?q={query}&appid={self.api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                return None
                
        except Exception as e:
            st.error(f"Error fetching forecast: {str(e)}")
            return None
    
    def render_current_weather(self, data, units="Celsius"):
        """Render current weather information"""
        if not data:
            return
            
        # Extract data
        city_name = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description'].title()
        wind_speed = data['wind']['speed']
        visibility = data.get('visibility', 0) / 1000
        icon_code = data['weather'][0]['icon']
        
        # Convert temperature if needed
        if units == "Fahrenheit":
            temp = (temp * 9/5) + 32
            feels_like = (feels_like * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Main weather card
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"""
            <div class="weather-card">
                <h2>{city_name}, {country}</h2>
                <h1>{temp:.1f}{temp_unit}</h1>
                <p style="font-size: 1.2rem;">{description}</p>
                <p>Feels like {feels_like:.1f}{temp_unit}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Weather metrics
        st.subheader("📊 Weather Details")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🌡 Temperature",
                value=f"{temp:.1f}{temp_unit}",
                delta=f"Feels like {feels_like:.1f}{temp_unit}"
            )
        
        with col2:
            st.metric(
                label="💧 Humidity",
                value=f"{humidity}%"
            )
        
        with col3:
            st.metric(
                label="🌪 Wind Speed",
                value=f"{wind_speed} m/s"
            )
        
        with col4:
            st.metric(
                label="🔍 Visibility",
                value=f"{visibility:.1f} km"
            )
        
        # Additional metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📏 Pressure",
                value=f"{pressure} hPa"
            )
        
        with col2:
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
            st.metric(
                label="🌅 Sunrise",
                value=sunrise
            )
        
        with col3:
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            st.metric(
                label="🌇 Sunset",
                value=sunset
            )
    
    def render_forecast(self, forecast_data, units="Celsius"):
        """Render 5-day weather forecast"""
        if not forecast_data:
            return
            
        st.subheader("📅 5-Day Forecast")
        
        # Process forecast data
        forecast_list = []
        for item in forecast_data['list'][:40]:  # Next 5 days (8 forecasts per day)
            forecast_list.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temp': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'description': item['weather'][0]['description'],
                'wind_speed': item['wind']['speed'],
                'icon': item['weather'][0]['icon']
            })
        
        df = pd.DataFrame(forecast_list)
        
        # Convert temperature if needed
        if units == "Fahrenheit":
            df['temp'] = (df['temp'] * 9/5) + 32
            df['feels_like'] = (df['feels_like'] * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Display daily forecast cards
        daily_forecasts = df.groupby(df['datetime'].dt.date).agg({
            'temp': ['min', 'max', 'mean'],
            'humidity': 'mean',
            'pressure': 'mean',
            'description': 'first',
            'wind_speed': 'mean'
        }).head(5)
        
        cols = st.columns(5)
        
        for i, (date, row) in enumerate(daily_forecasts.iterrows()):
            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card">
                    <h4>{date.strftime('%a, %b %d')}</h4>
                    <p><strong>{row[('temp', 'max')]:.1f}{temp_unit}</strong></p>
                    <p style="color: #666;">{row[('temp', 'min')]:.1f}{temp_unit}</p>
                    <p style="font-size: 0.9rem;">{row[('description', 'first')].title()}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_charts(self, forecast_data, units="Celsius"):
        """Render weather charts"""
        if not forecast_data:
            return
            
        st.subheader("📈 Weather Charts")
        
        # Process data for charts
        chart_data = []
        for item in forecast_data['list'][:40]:
            chart_data.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed']
            })
        
        df = pd.DataFrame(chart_data)
        
        # Convert temperature if needed
        if units == "Fahrenheit":
            df['temperature'] = (df['temperature'] * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Temperature chart
        fig_temp = px.line(df, x='datetime', y='temperature', 
                          title=f'Temperature Forecast ({temp_unit})',
                          labels={'temperature': f'Temperature ({temp_unit})', 'datetime': 'Date & Time'})
        fig_temp.update_layout(height=400)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Combined metrics chart
        col1, col2 = st.columns(2)
        
        with col1:
            fig_humidity = px.line(df, x='datetime', y='humidity', 
                                  title='Humidity Forecast (%)',
                                  labels={'humidity': 'Humidity (%)', 'datetime': 'Date & Time'})
            fig_humidity.update_layout(height=300)
            st.plotly_chart(fig_humidity, use_container_width=True)
        
        with col2:
            fig_wind = px.line(df, x='datetime', y='wind_speed', 
                              title='Wind Speed Forecast (m/s)',
                              labels={'wind_speed': 'Wind Speed (m/s)', 'datetime': 'Date & Time'})
            fig_wind.update_layout(height=300)
            st.plotly_chart(fig_wind, use_container_width=True)
    
    def render_sample_data(self):
        """Render sample data when API key is not configured"""
        st.warning("⚠ API key not configured. Showing sample data.")
        
        # Sample current weather
        st.markdown("""
        <div class="weather-card">
            <h2>London, GB</h2>
            <h1>20.5°C</h1>
            <p style="font-size: 1.2rem;">Partly Cloudy</p>
            <p>Feels like 22.0°C</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample metrics
        st.subheader("📊 Weather Details")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🌡 Temperature", "20.5°C", "Feels like 22.0°C")
        with col2:
            st.metric("💧 Humidity", "65%")
        with col3:
            st.metric("🌪 Wind Speed", "3.5 m/s")
        with col4:
            st.metric("🔍 Visibility", "10.0 km")
        
        # Sample forecast
        st.subheader("📅 5-Day Forecast")
        cols = st.columns(5)
        
        sample_forecast = [
            ("Mon, Jul 8", "22°C", "18°C", "Sunny"),
            ("Tue, Jul 9", "24°C", "19°C", "Partly Cloudy"),
            ("Wed, Jul 10", "21°C", "16°C", "Rainy"),
            ("Thu, Jul 11", "23°C", "18°C", "Cloudy"),
            ("Fri, Jul 12", "25°C", "20°C", "Sunny")
        ]
        
        for i, (date, high, low, desc) in enumerate(sample_forecast):
            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card">
                    <h4>{date}</h4>
                    <p><strong>{high}</strong></p>
                    <p style="color: #666;">{low}</p>
                    <p style="font-size: 0.9rem;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def run(self):
        """Main function to run the Streamlit app"""
        self.setup_page()
        self.render_header()
        
        # Sidebar
        city, country, search_button = self.render_search_section()
        units, show_forecast, show_charts = self.render_sidebar_info()
        
        # Main content
        if self.api_key == "YOUR_API_KEY_HERE":
            self.render_sample_data()
        else:
            if search_button or city:
                # Get current weather
                weather_data = self.get_weather_data(city, country)
                
                if weather_data:
                    self.render_current_weather(weather_data, units)
                    
                    # Get forecast if requested
                    if show_forecast:
                        forecast_data = self.get_forecast_data(city, country)
                        if forecast_data:
                            self.render_forecast(forecast_data, units)
                    
                    # Show charts if requested
                    if show_charts and show_forecast:
                        forecast_data = self.get_forecast_data(city, country)
                        if forecast_data:
                            self.render_charts(forecast_data, units)
                else:
                    st.error("❌ Could not fetch weather data. Please check your input and try again.")
            else:
                st.info("👆 Enter a city name in the sidebar and click 'Get Weather' to start!")


def main():
    """Main function"""
    app = StreamlitWeatherApp()
    app.run()


if _name_ == "_main_":
    main()
