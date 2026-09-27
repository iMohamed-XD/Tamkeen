import datetime
import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("WEATHER_API_KEY is not set")
def get_weather_data(city: str) -> dict | None:
    URL = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q=bulk"

    headers = {
        'Content-Type': 'application/json',
    }

    payload = {
        "locations": [
                {
                "q": city,
            },
        ]
    }
    try:
        response = requests.post(URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        for entry in result["bulk"]:
            if "error" in entry:
                print(f"Failed: {entry['error']['message']}")
                continue
            query_result = entry['query']
            current = query_result['current']
            location = query_result['location']

            Condition = current['condition']['text']
            Humidity = current['humidity']
            Temperature = current['temp_c']
            Wind_Speed = current['wind_kph']

            City = location['name']
            Country = location['country']
        return {
            "Condition": Condition,
            "Humidity": Humidity,
            "Temperature": Temperature,
            "Wind_Speed": Wind_Speed,
            "City": City,
            "Country": Country,
        }
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        status_code = e.response.status_code
        if status_code == 401:
            print("Unauthorized: Check your API key.")
        elif status_code == 403:
            print("Forbidden: You might not have access to this model.")
        else:
            print(f"HTTP error occurred: {e.response.text} status code: {status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")

    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    except (KeyError, TypeError, ValueError) as e:
        print(f"An unexpected error occurred: {e}")

    return None

def get_forcast_data(city:str, days:int = 3) -> dict | None:
    URL = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": API_KEY,
        "q": city,
        "days": days
    }
    try:
        response = requests.get(URL, params=params, timeout=30)
        response.raise_for_status()
        result = response.json()
        return {
            "city": result["location"]["name"],
            "country": result["location"]["country"],
            "forecast": [
                {
                    "date": day["date"],
                    "avg_temp_c": day["day"]["avgtemp_c"],
                    "condition": day["day"]["condition"]["text"]
                }
                for day in result["forecast"]["forecastday"]
            ]
        }
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        status_code = e.response.status_code
        if status_code == 401:
            print("Unauthorized: Check your API key.")
        elif status_code == 403:
            print("Forbidden: You might not have access to this model.")
        else:
            print(f"HTTP error occurred: {e.response.text} status code: {status_code}")

    except requests.exceptions.ConnectionError as e:
        print(f"Connection error occurred: {e}")

    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    except (KeyError, TypeError, ValueError) as e:
        print(f"An unexpected error occurred: {e}")

    return None

def print_city(city:dict) -> None:
    print(f"Weather data for {city["City"]} {city["Country"]}:")
    print(f"Condition: {city['Condition']}")
    print(f"Humidity: {city['Humidity']}%")
    print(f"Temperature: {city['Temperature']}°C")
    print(f"Wind Speed: {city['Wind_Speed']} kph")
if __name__ == "__main__":
    cities:list[list] = []
    while True:
        print("Welcome to the Weather API!")
        choice = int(input("""
            1. Search city weather
            2. Show last searched city
            3. Show prev cities results
            4. Show City Forecast 
            5. Exit
        """))
        if choice == 1:
            city_name = input("Enter city name")
            weather_data = get_weather_data(city_name)
            if weather_data:
                cities.append([city_name, weather_data])
                print_city(weather_data)
            else:
                print("Failed to retrieve weather data.")
        elif choice == 2:
            print_city(cities[-1][-1])
        elif choice == 3:
            for city in cities:
                print(f"City: {city[0]}, Weather Data: {city[1]['Temperature']}")
        elif choice == 4:
            city_name = input("Enter city name for forecast: \n")
            days = int(input("Enter number of days for forecast (1-3): \n"))
            forecast_data = get_forcast_data(city_name, days)
            if forecast_data:
                print(f"\n===== 3-Day Forecast for {forecast_data['city']}, {forecast_data['country']} =====\n")
                for i, day in enumerate(forecast_data["forecast"]):
                    parsed = datetime.datetime.strptime(day["date"], "%Y-%m-%d").replace(
                        tzinfo=datetime.timezone.utc
                    )
                    if i == 0:
                        label = "Today"
                    elif i == 1:
                        label = "Tomorrow"
                    else:
                        label = parsed.strftime("%A")
                    print(f"{label:<12}{day['avg_temp_c']}°C   {day['condition']}")
            else:
                print("Failed to retrieve forecast data.")
        elif choice == 5:
            print("Exiting the program.")
            break