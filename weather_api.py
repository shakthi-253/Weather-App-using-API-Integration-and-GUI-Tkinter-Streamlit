weather_api.py
#!/usr/bin/env python3
"""
Weather API Module
Handles all weather API interactions and data processing
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WeatherAPI:
    """Weather API handler class"""
    
    def _init_(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.icon_url = "https://openweathermap.org/img/wn"
        
    def get_current_weather(self, city: str, country: str = "", units: str = "metric") -> Optional[Dict]:
        """
        Get current weather for a city
        
        Args:
            city: City name
            country: Country code (optional)
            units: Temperature units (metric, imperial, kelvin)
            
        Returns:
            Weather data dictionary or None if error
        """
        try:
            query = f"{city},{country}" if country else city
            url = f"{self.base_url}/weather"
            
            params = {
                'q': query,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching weather: {str(e)}")
    
    def get_forecast(self, city: str, country: str = "", units: str = "metric") -> Optional[Dict]:
        """
        Get 5-day weather forecast
        
        Args:
            city: City name
            country: Country code (optional)
            units: Temperature units (metric, imperial, kelvin)
            
        Returns:
            Forecast data dictionary or None if error
        """
        try:
            query = f"{city},{country}" if country else city
            url = f"{self.base_url}/forecast"
            
            params = {
                'q': query,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching forecast: {str(e)}")
    
    def get_weather_by_coordinates(self, lat: float, lon: float, units: str = "metric") -> Optional[Dict]:
        """
        Get weather by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units
            
        Returns:
            Weather data dictionary or None if error
        """
        try:
            url = f"{self.base_url}/weather"
            
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching weather: {str(e)}")
    
    def geocode_city(self, city: str, country: str = "", limit: int = 1) -> List[Dict]:
        """
        Get coordinates for a city
        
        Args:
            city: City name
            country: Country code (optional)
            limit: Maximum number of results
            
        Returns:
            List of location dictionaries
        """
        try:
            query = f"{city},{country}" if country else city
            url = f"{self.geocoding_url}/direct"
            
            params = {
                'q': query,
                'limit': limit,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"Geocoding error: {error_data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error geocoding city: {str(e)}")
    
    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get air pollution data
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Air pollution data dictionary or None if error
        """
        try:
            url = f"{self.base_url}/air_pollution"
            
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json()
                raise Exception(f"API Error: {error_data.get('message', 'Unknown error')}")
                
        except requests.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching air pollution: {str(e)}")
    
    def get_icon_url(self, icon_code: str, size: str = "2x") -> str:
        """
        Get weather icon URL
        
        Args:
            icon_code: Weather icon code
            size: Icon size (1x, 2x, 4x)
            
        Returns:
            Icon URL
        """
        return f"{self.icon_url}/{icon_code}@{size}.png"
    
    def format_weather_data(self, data: Dict) -> Dict:
        """
        Format weather data for display
        
        Args:
            data: Raw weather data from API
            
        Returns:
            Formatted weather data dictionary
        """
        if not data:
            return {}
            
        try:
            formatted = {
                'location': {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'coordinates': {
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon']
                    }
                },
                'current': {
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'].title(),
                    'main': data['weather'][0]['main'],
                    'icon': data['weather'][0]['icon']
                },
                'wind': {
                    'speed': data['wind']['speed'],
                    'direction': data['wind'].get('deg', 0),
                    'gust': data['wind'].get('gust', 0)
                },
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'sun': {
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                },
                'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return formatted
            
        except KeyError as e:
            raise Exception(f"Data formatting error: {str(e)}")
    
    def format_forecast_data(self, data: Dict) -> List[Dict]:
        """
        Format forecast data for display
        
        Args:
            data: Raw forecast data from API
            
        Returns:
            List of formatted forecast entries
        """
        if not data or 'list' not in data:
            return []
            
        try:
            formatted_list = []
            
            for item in data['list']:
                formatted = {
                    'datetime': datetime.fromtimestamp(item['dt']),
                    'temperature': {
                        'temp': round(item['main']['temp'], 1),
                        'feels_like': round(item['main']['feels_like'], 1),
                        'min': round(item['main']['temp_min'], 1),
                        'max': round(item['main']['temp_max'], 1)
                    },
                    'weather': {
                        'main': item['weather'][0]['main'],
                        'description': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon']
                    },
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind': {
                        'speed': item['wind']['speed'],
                        'direction': item['wind'].get('deg', 0),
                        'gust': item['wind'].get('gust', 0)
                    },
                    'visibility': item.get('visibility', 0) / 1000,
                    'precipitation': item.get('rain', {}).get('3h', 0) + item.get('snow', {}).get('3h', 0)
                }
                
                formatted_list.append(formatted)
            
            return formatted_list
            
        except KeyError as e:
            raise Exception(f"Forecast formatting error: {str(e)}")
    
    def get_daily_forecast(self, forecast_data: List[Dict], days: int = 5) -> List[Dict]:
        """
        Convert 3-hourly forecast to daily forecast
        
        Args:
            forecast_data: Formatted forecast data
            days: Number of days to return
            
        Returns:
            List of daily forecast dictionaries
        """
        if not forecast_data:
            return []
            
        daily_forecast = []
        current_date = None
        day_data = []
        
        for item in forecast_data:
            item_date = item['datetime'].date()
            
            if current_date is None:
                current_date = item_date
                
            if item_date == current_date:
                day_data.append(item)
            else:
                # Process previous day
                if day_data:
                    daily_forecast.append(self._process_daily_data(day_data))
                    
                # Start new day
                current_date = item_date
                day_data = [item]
                
                if len(daily_forecast) >= days:
                    break
        
        # Process last day
        if day_data and len(daily_forecast) < days:
            daily_forecast.append(self._process_daily_data(day_data))
        
        return daily_forecast[:days]
    
    def _process_daily_data(self, day_data: List[Dict]) -> Dict:
        """
        Process a day's worth of forecast data
        
        Args:
            day_data: List of forecast entries for one day
            
        Returns:
            Daily summary dictionary
        """
        if not day_data:
            return {}
            
        date = day_data[0]['datetime'].date()
        temperatures = [item['temperature']['temp'] for item in day_data]
        
        return {
            'date': date,
            'temperature': {
                'min': min(temperatures),
                'max': max(temperatures),
                'avg': sum(temperatures) / len(temperatures)
            },
            'weather': day_data[len(day_data)//2]['weather'],  # Use middle forecast for weather
            'humidity': sum(item['humidity'] for item in day_data) / len(day_data),
            'wind_speed': sum(item['wind']['speed'] for item in day_data) / len(day_data),
            'precipitation': sum(item['precipitation'] for item in day_data)
        }


def get_sample_weather_data() -> Dict:
    """
    Get sample weather data for demonstration
    
    Returns:
        Sample weather data dictionary
    """
    return {
        'location': {
            'city': 'London',
            'country': 'GB',
            'coordinates': {'lat': 51.5074, 'lon': -0.1278}
        },
        'current': {
            'temperature': 20.5,
            'feels_like': 22.0,
            'humidity': 65,
            'pressure': 1013,
            'description': 'Partly Cloudy',
            'main': 'Clouds',
            'icon': '02d'
        },
        'wind': {
            'speed': 3.5,
            'direction': 270,
            'gust': 5.0
        },
        'visibility': 10.0,
        'sun': {
            'sunrise': '06:30',
            'sunset': '20:15'
        },
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def get_sample_forecast_data() -> List[Dict]:
    """
    Get sample forecast data for demonstration
    
    Returns:
        List of sample forecast entries
    """
    base_date = datetime.now()
    forecast_data = []
    
    for i in range(40):  # 5 days * 8 forecasts per day
        forecast_time = base_date + timedelta(hours=i * 3)
        
        # Simple temperature variation
        temp_base = 20 + (i % 8 - 4) * 2  # Varies throughout the day
        temp_variation = (i // 8) * 1  # Slight trend over days
        
        forecast_data.append({
            'datetime': forecast_time,
            'temperature': {
                'temp': temp_base + temp_variation,
                'feels_like': temp_base + temp_variation + 2,
                'min': temp_base + temp_variation - 2,
                'max': temp_base + temp_variation + 2
            },
            'weather': {
                'main': 'Clouds',
                'description': 'Partly Cloudy',
                'icon': '02d'
            },
            'humidity': 60 + (i % 5) * 5,
            'pressure': 1013 + (i % 3) * 2,
            'wind': {
                'speed': 3 + (i % 4),
                'direction': 270,
                'gust': 5
            },
            'visibility': 10.0,
            'precipitation': 0
        })
    
    return forecast_data
