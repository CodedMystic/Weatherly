import tkinter as tk
from tkinter import messagebox
import requests

weather_codes = {
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Foggy",
    51: "Drizzle",
    61: "Rain",
    71: "Snow",
    80: "Rain Showers",
    95: "Thunderstorm"
}

def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Weatherly", "Enter a city name")
        return

    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "format": "json"
            }
        ).json()

        if "results" not in geo:
            messagebox.showerror("Weatherly", "City not found")
            return

        location = geo["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]

        data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min",
                "forecast_days": 5,
                "timezone": "auto"
            }
        ).json()

        current = data["current"]
        daily = data["daily"]

        location_label.config(
            text=f"{location['name']}, {location.get('country', '')}"
        )

        temperature.config(
            text=f"{current['temperature_2m']:.0f}°C"
        )

        condition.config(
            text=weather_codes.get(
                current["weather_code"],
                "Unknown"
            )
        )

        details.config(
            text=f"Humidity  {current['relative_humidity_2m']}%     "
                 f"Wind  {current['wind_speed_10m']:.0f} km/h"
        )

        for widget in forecast.winfo_children():
            widget.destroy()

        for i in range(5):
            card = tk.Frame(
                forecast,
                bg="#ffffff",
                padx=8,
                pady=12
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=4
            )

            day = daily["time"][i]

            tk.Label(
                card,
                text=day[5:],
                bg="#ffffff",
                fg="#222222",
                font=("Segoe UI", 9, "bold")
            ).pack()

            tk.Label(
                card,
                text=weather_codes.get(
                    daily["weather_code"][i],
                    "Unknown"
                ),
                bg="#ffffff",
                fg="#777777",
                font=("Segoe UI", 8)
            ).pack(pady=7)

            tk.Label(
                card,
                text=f"{daily['temperature_2m_max'][i]:.0f}°",
                bg="#ffffff",
                fg="#222222",
                font=("Segoe UI", 13, "bold")
            ).pack()

            tk.Label(
                card,
                text=f"{daily['temperature_2m_min'][i]:.0f}°",
                bg="#ffffff",
                fg="#999999",
                font=("Segoe UI", 9)
            ).pack(pady=(2, 0))

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Weatherly",
            "No internet connection"
        )

    except Exception:
        messagebox.showerror(
            "Weatherly",
            "Something went wrong"
        )

root = tk.Tk()
root.title("Weatherly")
root.geometry("620x650")
root.resizable(False, False)
root.configure(bg="#eef3f8")

header = tk.Frame(
    root,
    bg="#172a46",
    height=115
)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="Weatherly",
    font=("Segoe UI", 25, "bold"),
    bg="#172a46",
    fg="white"
).pack(pady=(20, 0))

tk.Label(
    header,
    text="Check the weather anywhere",
    font=("Segoe UI", 9),
    bg="#172a46",
    fg="#b9c7d8"
).pack(pady=(2, 0))

search = tk.Frame(
    root,
    bg="#eef3f8"
)
search.pack(pady=18)

city_entry = tk.Entry(
    search,
    width=28,
    font=("Segoe UI", 11),
    bg="white",
    fg="#222222",
    insertbackground="#222222",
    relief="flat",
    bd=0
)
city_entry.pack(
    side="left",
    ipady=9,
    padx=(0, 7)
)

search_button = tk.Button(
    search,
    text="Search",
    command=get_weather,
    font=("Segoe UI", 10, "bold"),
    bg="#172a46",
    fg="white",
    activebackground="#263d5e",
    activeforeground="white",
    relief="flat",
    bd=0,
    padx=18,
    pady=8,
    cursor="hand2"
)
search_button.pack(side="left")

card = tk.Frame(
    root,
    bg="white",
    height=205
)
card.pack(
    padx=40,
    fill="x"
)
card.pack_propagate(False)

location_label = tk.Label(
    card,
    text="Enter a city",
    font=("Segoe UI", 16, "bold"),
    bg="white",
    fg="#222222"
)
location_label.pack(pady=(18, 0))

temperature = tk.Label(
    card,
    text="--°C",
    font=("Segoe UI", 42, "bold"),
    bg="white",
    fg="#172a46"
)
temperature.pack()

condition = tk.Label(
    card,
    text="Search for weather",
    font=("Segoe UI", 12),
    bg="white",
    fg="#666666"
)
condition.pack()

details = tk.Label(
    card,
    text="Humidity  --     Wind  --",
    font=("Segoe UI", 9),
    bg="white",
    fg="#888888"
)
details.pack(pady=12)

tk.Label(
    root,
    text="5-Day Forecast",
    font=("Segoe UI", 16, "bold"),
    bg="#eef3f8",
    fg="#222222"
).pack(pady=(20, 12))

forecast = tk.Frame(
    root,
    bg="#eef3f8",
    height=145
)
forecast.pack(
    padx=32,
    fill="x"
)
forecast.pack_propagate(False)

root.mainloop()