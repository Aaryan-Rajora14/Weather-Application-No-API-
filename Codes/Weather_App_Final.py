import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
from PIL import Image, ImageTk, ImageOps
from io import BytesIO
import datetime
from warnings import filterwarnings
filterwarnings("ignore")

class ModernWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast Pro")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.root.minsize(900, 650)
        
        # Colors
        self.bg_color = "#a7a7a7"
        self.card_color = "#71ADDD"
        self.accent_color = "#4682b4"
        self.text_color = "#333333"
        
        # Fonts
        self.title_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.normal_font = font.Font(family="Segoe UI", size=10)
        self.small_font = font.Font(family="Segoe UI", size=9)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Create GUI
        self.create_widgets()
        
        # Set default icon
        self.set_default_icon()

    def configure_styles(self):
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        self.style.configure('TButton', font=self.normal_font, padding=6)
        self.style.configure('TEntry', font=self.normal_font, padding=5)
        self.style.configure('TRadiobutton', font=self.normal_font, background=self.bg_color)
        self.style.configure('TLabelFrame', font=self.title_font, relief=tk.GROOVE, borderwidth=2)
        self.style.configure('Card.TFrame', background=self.card_color, relief=tk.RAISED, borderwidth=1)
        self.style.configure('Accent.TButton', background=self.accent_color, foreground='white')
        self.style.map('Accent.TButton',
                      background=[('active', '#5a9bd5'), ('pressed', '#3a6b99')])

    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        self.header_frame = ttk.Frame(self.main_container)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.header_frame, text="Weather Forecast Pro", 
                 font=("Segoe UI", 18, "bold")).pack(side=tk.LEFT)
        
        # Search frame
        self.search_frame = ttk.LabelFrame(self.main_container, text="Search Location")
        self.search_frame.pack(fill=tk.X, pady=5)
        
        # City entry
        ttk.Label(self.search_frame, text="City:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.city_entry = ttk.Entry(self.search_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.city_entry.bind("<Return>", lambda e: self.get_weather())
        
        # Units selection
        ttk.Label(self.search_frame, text="Units:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.unit_var = tk.StringVar(value="m")  # m = metric, u = imperial
        ttk.Radiobutton(self.search_frame, text="Celsius (°C)", variable=self.unit_var, 
                        value="m").grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(self.search_frame, text="Fahrenheit (°F)", variable=self.unit_var, 
                        value="u").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        
        # Search button
        self.search_btn = ttk.Button(
            self.search_frame,
            text="Get Weather",
            style="Accent.TButton",
            command=self.get_weather
        )
        self.search_btn.grid(row=0, column=3, rowspan=2, padx=10, pady=5, sticky=tk.E)
        
        # Weather display area
        self.weather_display = ttk.Frame(self.main_container)
        self.weather_display.pack(fill=tk.BOTH, expand=True)
        
        # Current weather card
        self.current_weather_card = ttk.Frame(self.weather_display, style="Card.TFrame")
        self.current_weather_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Weather icon and main info
        self.weather_icon_frame = ttk.Frame(self.current_weather_card)
        self.weather_icon_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.weather_icon = ttk.Label(self.weather_icon_frame)
        self.weather_icon.pack()
        
        # Weather details
        self.weather_details = ttk.Frame(self.current_weather_card)
        self.weather_details.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.location_label = ttk.Label(self.weather_details, text="Location: ", font=('Segoe UI', 12, 'bold'))
        self.location_label.pack(anchor=tk.W)
        
        self.temp_label = ttk.Label(self.weather_details, text="Temperature: ", font=self.normal_font)
        self.temp_label.pack(anchor=tk.W)
        
        self.feels_like_label = ttk.Label(self.weather_details, text="Feels like: ", font=self.normal_font)
        self.feels_like_label.pack(anchor=tk.W)
        
        self.conditions_label = ttk.Label(self.weather_details, text="Conditions: ", font=self.normal_font)
        self.conditions_label.pack(anchor=tk.W)
        
        self.wind_label = ttk.Label(self.weather_details, text="Wind: ", font=self.normal_font)
        self.wind_label.pack(anchor=tk.W)
        
        self.humidity_label = ttk.Label(self.weather_details, text="Humidity: ", font=self.normal_font)
        self.humidity_label.pack(anchor=tk.W)
        
        self.pressure_label = ttk.Label(self.weather_details, text="Pressure: ", font=self.normal_font)
        self.pressure_label.pack(anchor=tk.W)
        
        self.visibility_label = ttk.Label(self.weather_details, text="Visibility: ", font=self.normal_font)
        self.visibility_label.pack(anchor=tk.W)
        
        # Additional info frame
        self.additional_info_frame = ttk.Frame(self.current_weather_card)
        self.additional_info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        self.sunrise_label = ttk.Label(self.additional_info_frame, text="Sunrise: ", font=self.normal_font)
        self.sunrise_label.pack(anchor=tk.W)
        
        self.sunset_label = ttk.Label(self.additional_info_frame, text="Sunset: ", font=self.normal_font)
        self.sunset_label.pack(anchor=tk.W)
        
        self.uv_index_label = ttk.Label(self.additional_info_frame, text="UV Index: ", font=self.normal_font)
        self.uv_index_label.pack(anchor=tk.W)
        
        # Forecast frame
        self.forecast_frame = ttk.LabelFrame(self.weather_display, text="3-Day Forecast")
        self.forecast_frame.pack(fill=tk.BOTH, pady=(10, 0))
        
        # Create forecast cards
        self.forecast_cards = []
        for i in range(3):
            card = ttk.Frame(self.forecast_frame, style="Card.TFrame")
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            day_label = ttk.Label(card, text=f"Day {i+1}", font=('Segoe UI', 10, 'bold'))
            day_label.pack(pady=(5, 0))
            
            icon_label = ttk.Label(card)
            icon_label.pack()
            
            temp_label = ttk.Label(card, font=self.normal_font)
            temp_label.pack()
            
            desc_label = ttk.Label(card, font=self.small_font)
            desc_label.pack()
            
            wind_label = ttk.Label(card, font=self.small_font)
            wind_label.pack()
            
            self.forecast_cards.append({
                'frame': card,
                'day': day_label,
                'icon': icon_label,
                'temp': temp_label,
                'desc': desc_label,
                'wind': wind_label
            })
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(
            self.main_container,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=self.small_font
        )
        self.status_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Configure grid weights
        self.search_frame.columnconfigure(1, weight=1)

    def get_weather(self):
        city = self.city_entry.get().strip()
        units = self.unit_var.get()

        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return

        self.status_var.set("Fetching weather data...")
        self.root.update()

        try:
            weather_data, forecast_data = self.fetch_weather_data(city, units)
            self.update_weather_display(weather_data, forecast_data)
            self.status_var.set(f"Weather data for {weather_data['location']} - Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to get weather data:\n{str(e)}")
            self.status_var.set("Error fetching weather data")
            self.clear_weather_display()

    def fetch_weather_data(self, city, units):
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, headers={'User-Agent': 'curl/7.64.1'}, timeout=10)
        json_data = response.json()

        current = json_data['current_condition'][0]
        area_info = json_data['nearest_area'][0]
        weather = json_data['weather'][0]

        temp = current['temp_C'] + " °C" if units == 'm' else current['temp_F'] + " °F"
        feels_like = current['FeelsLikeC'] + " °C" if units == 'm' else current['FeelsLikeF'] + " °F"
        wind_speed = current['windspeedKmph'] + " km/h" if units == 'm' else str(round(float(current['windspeedKmph']) * 0.621371, 1)) + " mph"
        
        # Get sunrise/sunset times
        astronomy = weather['astronomy'][0]
        sunrise = astronomy['sunrise']
        sunset = astronomy['sunset']

        weather_data = {
            'location': f"{area_info['areaName'][0]['value']}, {area_info['region'][0]['value']}, {area_info['country'][0]['value']}",
            'temp': temp,
            'feels_like': feels_like,
            'conditions': current['weatherDesc'][0]['value'],
            'wind': wind_speed + f", {current['winddir16Point']}",
            'humidity': current['humidity'] + "%",
            'pressure': current['pressure'] + " hPa",
            'visibility': current['visibility'] + " km",
            'uv_index': current['uvIndex'],
            'sunrise': sunrise,
            'sunset': sunset,
            'icon_url': f"https://wttr.in/{city}_0p.png"
        }

        forecast_data = []
        for day in json_data['weather'][:3]:
            avg_temp = day['avgtempC'] + " °C" if units == 'm' else day['avgtempF'] + " °F"
            max_temp = day['maxtempC'] + " °C" if units == 'm' else day['maxtempF'] + " °F"
            min_temp = day['mintempC'] + " °C" if units == 'm' else day['mintempF'] + " °F"
            
            forecast_data.append({
                'date': day['date'],
                'day_name': datetime.datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A'),
                'avgtemp': avg_temp,
                'maxtemp': max_temp,
                'mintemp': min_temp,
                'desc': day['hourly'][4]['weatherDesc'][0]['value'],
                'wind': day['hourly'][4]['windspeedKmph'] + " km/h",
                'icon_url': f"https://wttr.in/{city}_{day['date']}_0p.png"
            })

        return weather_data, forecast_data

    def update_weather_display(self, weather_data, forecast_data):
        # Update current weather
        self.location_label.config(text=f"{weather_data['location']}")
        self.temp_label.config(text=f"Temperature: {weather_data['temp']}")
        self.feels_like_label.config(text=f"Feels like: {weather_data['feels_like']}")
        self.conditions_label.config(text=f"Conditions: {weather_data['conditions']}")
        self.wind_label.config(text=f"Wind: {weather_data['wind']}")
        self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}")
        self.pressure_label.config(text=f"Pressure: {weather_data['pressure']}")
        self.visibility_label.config(text=f"Visibility: {weather_data['visibility']}")
        self.sunrise_label.config(text=f"Sunrise: {weather_data['sunrise']}")
        self.sunset_label.config(text=f"Sunset: {weather_data['sunset']}")
        self.uv_index_label.config(text=f"UV Index: {weather_data['uv_index']}")

        if 'icon_url' in weather_data:
            self.load_weather_icon(weather_data['icon_url'], self.weather_icon, (400, 300))

        # Update forecast
        for i, day in enumerate(forecast_data[:3]):
            card = self.forecast_cards[i]
            card['day'].config(text=f"{day['day_name']} ({day['date']})")
            card['temp'].config(text=f"Avg: {day['avgtemp']}\nMax: {day['maxtemp']}\nMin: {day['mintemp']}")
            card['desc'].config(text=day['desc'])
            card['wind'].config(text=f"Wind: {day['wind']}")
            
            if 'icon_url' in day:
                self.load_weather_icon(day['icon_url'], card['icon'], (100, 100))

    def load_weather_icon(self, url, label, size):
        try:
            response = requests.get(url, headers={'User-Agent': 'curl/7.64.1'}, timeout=5)
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            
            # Add rounded corners and drop shadow
            img = img.resize(size, Image.LANCZOS)
            img = ImageOps.expand(img, border=2, fill="#e0e0e0")
            
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo
        except Exception as e:
            print(f"Error loading weather icon: {e}")
            self.set_default_icon(label, size)

    def set_default_icon(self, label=None, size=(200, 200)):
        if label is None:
            label = self.weather_icon
        blank_img = Image.new('RGBA', size, (240, 240, 240, 0))
        photo = ImageTk.PhotoImage(blank_img)
        label.config(image=photo)
        label.image = photo

    def clear_weather_display(self):
        self.location_label.config(text="Location: ")
        self.temp_label.config(text="Temperature: ")
        self.feels_like_label.config(text="Feels like: ")
        self.conditions_label.config(text="Conditions: ")
        self.wind_label.config(text="Wind: ")
        self.humidity_label.config(text="Humidity: ")
        self.pressure_label.config(text="Pressure: ")
        self.visibility_label.config(text="Visibility: ")
        self.sunrise_label.config(text="Sunrise: ")
        self.sunset_label.config(text="Sunset: ")
        self.uv_index_label.config(text="UV Index: ")
        
        for card in self.forecast_cards:
            card['day'].config(text="")
            card['temp'].config(text="")
            card['desc'].config(text="")
            card['wind'].config(text="")
            self.set_default_icon(card['icon'], (100, 100))
        
        self.set_default_icon()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernWeatherApp(root)
    root.mainloop()