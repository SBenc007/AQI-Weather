import json
import requests
import folium
import main_functions

"""Task 6"""
def get_api_key(filename):
    with open(filename) as file:
        data = json.load(file)
        api_key = data["aqi_api_key"]
    return api_key

my_aqi_api_key = get_api_key("api_key.json")
print(my_aqi_api_key)


"""Task 7"""
def get_aqi_data(api_key):
    url = f"http://api.airvisual.com/v2/nearest_city?key={api_key}"
    response = requests.get(url)
    data = response.json()

    with open("aqi.json", "w") as file:
        json.dump(data, file)

get_aqi_data(my_aqi_api_key)


"""Task 8"""
def generate_map(data_filename,zoom_start):
    aqi_data = main_functions.read_from_file(data_filename)
    lat = 25.761681
    long = -80.191788
    m = folium.Map(location=[lat, long], zoom_start=zoom_start)
    folium.Marker(
        location=[lat, long],
        popup='AQI Station',
        icon=folium.Icon()
    ).add_to(m)
    m.save("map.html")

generate_map("aqi.json",10)


"""Task 9"""
def display_aqi_info(data_filename):
    aqi_data = main_functions.read_from_file(data_filename)
    tempC = aqi_data["data"]["current"]["weather"]["tp"]
    tempF = tempC * 1.8 + 32
    humid = aqi_data["data"]["current"]["weather"]["hu"]
    aqius = aqi_data["data"]["current"]["pollution"]["aqius"]

    air_quality = get_air_quality(aqius)

    print(f"The temperature is {tempC}ºC or {tempF}ºF, the humidity is {humid}%, and the index shows that the air quality is {air_quality}.")

def get_air_quality(aqius):
    if aqius >= 0 and aqius <= 50:
        return "good"
    elif aqius >= 51 and aqius <= 100:
        return "moderate"
    elif aqius >= 101 and aqius <= 150:
        return "unhealthy for sensitive groups"
    elif aqius >= 151 and aqius <= 200:
        return "unhealthy"
    elif aqius >= 201 and aqius <= 300:
        return "very unhealthy"
    else:
        return "unknown"

display_aqi_info("aqi.json")