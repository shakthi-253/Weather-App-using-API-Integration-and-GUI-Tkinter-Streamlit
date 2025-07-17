weather  _app.py
#!/usr/bin/env python3
"""
Weather App with Tkinter GUI
A comprehensive weather application that fetches real-time weather data
and displays it in a user-friendly interface.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import os
from io import BytesIO
import threading


class WeatherApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Weather API configuration
        self.api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        
        # Create the interface
        self.create_widgets()
        
        # Load default weather
        self.load_default_weather()
    
    def create_widgets(self):
        """Create and arrange all GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        title_label = tk.Label(main_frame, text="Weather App", 
                              font=title_font, bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg='#2c3e50')
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # City input
        self.city_var = tk.StringVar()
        city_label = tk.Label(search_frame, text="Enter City:", 
                             font=("Helvetica", 12), bg='#2c3e50', fg='#ecf0f1')
        city_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.city_entry = tk.Entry(search_frame, textvariable=self.city_var, 
                                  font=("Helvetica", 12), width=30)
        self.city_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.city_entry.bind('<Return>', self.on_search)
        
        # Search button
        search_btn = tk.Button(search_frame, text="Get Weather", 
                              command=self.get_weather, 
                              font=("Helvetica", 12), 
                              bg='#3498db', fg='white',
                              relief=tk.FLAT, padx=20)
        search_btn.pack(side=tk.LEFT)
        
        # Weather display frame
        self.weather_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        self.weather_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create weather display widgets
        self.create_weather_display()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(main_frame, textvariable=self.status_var, 
                             relief=tk.SUNKEN, anchor=tk.W, 
                             bg='#2c3e50', fg='#ecf0f1')
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_weather_display(self):
        """Create the weather information display area"""
        # City name
        self.city_label = tk.Label(self.weather_frame, text="City Name", 
                                  font=("Helvetica", 20, "bold"), 
                                  bg='#34495e', fg='#ecf0f1')
        self.city_label.pack(pady=(20, 10))
        
        # Weather icon and main info frame
        main_info_frame = tk.Frame(self.weather_frame, bg='#34495e')
        main_info_frame.pack(pady=10)
        
        # Weather icon
        self.weather_icon = tk.Label(main_info_frame, bg='#34495e')
        self.weather_icon.pack(side=tk.LEFT, padx=20)
        
        # Temperature and description
        temp_frame = tk.Frame(main_info_frame, bg='#34495e')
        temp_frame.pack(side=tk.LEFT, padx=20)
        
        self.temp_label = tk.Label(temp_frame, text="--°C", 
                                  font=("Helvetica", 36, "bold"), 
                                  bg='#34495e', fg='#e74c3c')
        self.temp_label.pack()
        
        self.desc_label = tk.Label(temp_frame, text="--", 
                                  font=("Helvetica", 14), 
                                  bg='#34495e', fg='#ecf0f1')
        self.desc_label.pack()
        
        # Weather details frame
        details_frame = tk.Frame(self.weather_frame, bg='#34495e')
        details_frame.pack(pady=20, padx=20, fill=tk.X)
        
        # Create detail labels
        self.create_detail_labels(details_frame)
        
    def create_detail_labels(self, parent):
        """Create detailed weather information labels"""
        # First row
        row1 = tk.Frame(parent, bg='#34495e')
        row1.pack(fill=tk.X, pady=5)
        
        self.feels_like_label = tk.Label(row1, text="Feels like: --°C", 
                                        font=("Helvetica", 11), 
                                        bg='#34495e', fg='#ecf0f1')
        self.feels_like_label.pack(side=tk.LEFT)
        
        self.humidity_label = tk.Label(row1, text="Humidity: --%", 
                                      font=("Helvetica", 11), 
                                      bg='#34495e', fg='#ecf0f1')
        self.humidity_label.pack(side=tk.RIGHT)
        
        # Second row
        row2 = tk.Frame(parent, bg='#34495e')
        row2.pack(fill=tk.X, pady=5)
        
        self.pressure_label = tk.Label(row2, text="Pressure: -- hPa", 
                                      font=("Helvetica", 11), 
                                      bg='#34495e', fg='#ecf0f1')
        self.pressure_label.pack(side=tk.LEFT)
        
        self.wind_label = tk.Label(row2, text="Wind: -- m/s", 
                                  font=("Helvetica", 11), 
                                  bg='#34495e', fg='#ecf0f1')
        self.wind_label.pack(side=tk.RIGHT)
        
        # Third row
        row3 = tk.Frame(parent, bg='#34495e')
        row3.pack(fill=tk.X, pady=5)
        
        self.visibility_label = tk.Label(row3, text="Visibility: -- km", 
                                        font=("Helvetica", 11), 
                                        bg='#34495e', fg='#ecf0f1')
        self.visibility_label.pack(side=tk.LEFT)
        
        self.uv_label = tk.Label(row3, text="UV Index: --", 
                                font=("Helvetica", 11), 
                                bg='#34495e', fg='#ecf0f1')
        self.uv_label.pack(side=tk.RIGHT)
        
    def on_search(self, event=None):
        """Handle Enter key press in search field"""
        self.get_weather()
    
    def get_weather(self):
        """Fetch weather data from API"""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        self.status_var.set("Fetching weather data...")
        self.root.update()
        
        # Run API request in a separate thread to avoid blocking GUI
        thread = threading.Thread(target=self.fetch_weather_data, args=(city,))
        thread.daemon = True
        thread.start()
    
    def fetch_weather_data(self, city):
        """Fetch weather data in a separate thread"""
        try:
            # Construct API URL
            url = f"{self.base_url}?q={city}&appid={self.api_key}&units=metric"
            
            # Make API request
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                # Update GUI in main thread
                self.root.after(0, self.update_weather_display, data)
                self.root.after(0, self.status_var.set, "Weather data updated successfully")
            else:
                error_msg = data.get('message', 'Unknown error')
                self.root.after(0, self.show_error, f"Error: {error_msg}")
                
        except requests.RequestException as e:
            self.root.after(0, self.show_error, f"Network error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.show_error, f"Unexpected error: {str(e)}")
    
    def update_weather_display(self, data):
        """Update the weather display with fetched data"""
        try:
            # Extract weather information
            city_name = data['name']
            country = data['sys']['country']
            temp = round(data['main']['temp'])
            feels_like = round(data['main']['feels_like'])
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            description = data['weather'][0]['description'].title()
            wind_speed = data['wind']['speed']
            visibility = data.get('visibility', 0) / 1000  # Convert to km
            icon_code = data['weather'][0]['icon']
            
            # Update labels
            self.city_label.config(text=f"{city_name}, {country}")
            self.temp_label.config(text=f"{temp}°C")
            self.desc_label.config(text=description)
            self.feels_like_label.config(text=f"Feels like: {feels_like}°C")
            self.humidity_label.config(text=f"Humidity: {humidity}%")
            self.pressure_label.config(text=f"Pressure: {pressure} hPa")
            self.wind_label.config(text=f"Wind: {wind_speed} m/s")
            self.visibility_label.config(text=f"Visibility: {visibility:.1f} km")
            self.uv_label.config(text="UV Index: --")
            
            # Load weather icon
            self.load_weather_icon(icon_code)
            
        except KeyError as e:
            self.show_error(f"Data parsing error: {str(e)}")
    
    def load_weather_icon(self, icon_code):
        """Load weather icon from OpenWeatherMap"""
        try:
            icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(icon_url, timeout=10)
            
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.weather_icon.config(image=photo)
                self.weather_icon.image = photo  # Keep a reference
            else:
                self.weather_icon.config(text="No Icon", fg='#ecf0f1')
                
        except Exception as e:
            self.weather_icon.config(text="No Icon", fg='#ecf0f1')
    
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Error", message)
        self.status_var.set("Error occurred")
    
    def load_default_weather(self):
        """Load default weather data"""
        self.city_var.set("London")
        if self.api_key != "YOUR_API_KEY_HERE":
            self.get_weather()
        else:
            self.show_sample_data()
    
    def show_sample_data(self):
        """Show sample weather data when API key is not configured"""
        self.city_label.config(text="Sample City, UK")
        self.temp_label.config(text="20°C")
        self.desc_label.config(text="Partly Cloudy")
        self.feels_like_label.config(text="Feels like: 22°C")
        self.humidity_label.config(text="Humidity: 65%")
        self.pressure_label.config(text="Pressure: 1013 hPa")
        self.wind_label.config(text="Wind: 3.5 m/s")
        self.visibility_label.config(text="Visibility: 10.0 km")
        self.uv_label.config(text="UV Index: 5")
        self.weather_icon.config(text="☀", font=("Helvetica", 40), fg='#f39c12')
        self.status_var.set("Showing sample data - Add your API key for real weather")


def main():
    """Main function to run the weather app"""
    root = tk.Tk()
    app = WeatherApp(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if _name_ == "_main_":
    main()
