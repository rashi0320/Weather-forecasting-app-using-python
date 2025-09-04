import requests
import json

def get_weather(city_name, api_key):
    """
    Fetches weather data for a given city using the OpenWeatherMap API.
    
    Args:
        city_name (str): The name of the city.
        api_key (str): Your OpenWeatherMap API key.

    Returns:
        dict: A dictionary containing weather information, or None if an error occurs.
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # Use "imperial" for Fahrenheit
    }

    try:
        # Make the GET request to the OpenWeatherMap API
        response = requests.get(base_url, params=params)
        
        # Raise an HTTPError for bad responses (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response
        weather_data = response.json()

        # Check if the city was not found
        if weather_data.get("cod") == "404":
            print("Error: City not found.")
            return None

        # Extract the relevant weather information
        main_weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        
        # Return a dictionary with the extracted data
        return {
            "description": main_weather,
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed
        }

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except (KeyError, IndexError) as json_err:
        print(f"Could not parse weather data. JSON structure may have changed: {json_err}")
    
    return None

if __name__ == "__main__":
    # You must get your own API key from OpenWeatherMap.
    # Visit https://openweathermap.org/api to sign up for a free account.
    API_KEY = "YOUR_API_KEY_HERE"  # Replace with your actual API key

    # Check if the API key is the default placeholder
    if API_KEY == "YOUR_API_KEY_HERE":
        print("Please replace 'YOUR_API_KEY_HERE' with your actual OpenWeatherMap API key.")
    else:
        city = input("Enter the city name to get its weather: ")
        
        weather = get_weather(city, API_KEY)
        
        if weather:
            print(f"\nWeather for {city.title()}:")
            print("-" * 30)
            print(f"Description: {weather['description'].title()}")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Humidity:    {weather['humidity']}%")
            print(f"Wind Speed:  {weather['wind_speed']} m/s")
            print("-" * 30)
