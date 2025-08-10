# Weather Forecast Pro

A modern desktop weather forecast application built with Python and Tkinter. It fetches weather data from the [wttr.in](https://wttr.in) API and displays current weather conditions and a 3-day forecast with icons in a clean, user-friendly interface.

## Features

- Search weather by city name
- Supports metric (Celsius, km/h) and imperial (Fahrenheit, mph) units
- Displays current temperature, feels like, conditions, wind, humidity, pressure, visibility, UV index, sunrise and sunset times
- Shows 3-day weather forecast with daily average, max, min temperatures, weather description, wind, and icons
- Responsive and modern GUI using Tkinter and themed widgets
- Weather icons loaded dynamically from wttr.in

## Requirements

- Python 3.x
- `requests` library
- `Pillow` (PIL) library for image handling

You can install the required libraries using pip:

```bash
pip install requests pillow
```

## Usage

1. Run the script:

```bash
python Weather_Practice.py
```

2. Enter the city name in the input box.
3. Select the units (Celsius or Fahrenheit).
4. Click the "Get Weather" button or press Enter.
5. View the current weather and 3-day forecast displayed in the app window.

## Notes

- The app uses the free wttr.in API to fetch weather data. No API key is required.
- Internet connection is required to fetch weather data and icons.
- The app handles errors such as invalid city names or network issues gracefully with error messages.

## License

This project is for educational and personal use.

---

Created with Python and Tkinter by [Your Name].
