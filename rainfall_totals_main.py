import folium
import requests

url = "https://archive-api.open-meteo.com/v1/archive"

locations = [
    {"name": "London", "latitude": 51.5074, "longitude": -0.1278},
    {"name": "Wrexham", "latitude": 53.045, "longitude": -2.991},
    {"name": "Cardiff", "latitude": 51.4816, "longitude": -3.1791},
    {"name": "Belfast", "latitude": 54.5973, "longitude": -5.9301},
    {"name": "Edinburgh", "latitude": 55.9533, "longitude": -3.1883}
]

table = []



def get_precipitation_data(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "past_days": 14,
        "daily": "precipitation_sum",
        "timezone": "GMT"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200: #200 is the HTTP status code for a successful request
        precipitation_data = response.json()
        #print(precipitation_data)
        return precipitation_data
    else:
        print(f"Request failed with status code: {response.status_code}")


for i in range(len(locations)): #Creates a table of precipitation for each location
    location = locations[i]
    precipitation_info = get_precipitation_data(location["latitude"], location["longitude"])
    total_precipitation = sum(precipitation_info['daily']['precipitation_sum'])
    
    table.append ({"location": location["name"], "total_precipitation": total_precipitation})





tiles_url = "https://basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png?key=(INSERT API KEY HERE)" #An API key needs to be supplied for the program to work

map = folium.Map(
    tiles=tiles_url, 
    location = (54.5, -3.5), #Set to UK
    zoom_start = 6, 
    min_zoom = 5,
    max_bounds = True, #Sets limits to how far you can zoom out, or move the map to retain UK focus
    min_lat=35,
    max_lat=65,
    min_lon=-14,
    max_lon=3,
    attr="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors &copy; <a href='https://www.carto.com/'>CARTO</a>" #Accreditation
    )

for i in range(len(table)): #Adds information circles onto the map

    if table[i]["total_precipitation"] > 38 and table[i]["total_precipitation"] < 58: #Standard precipitation
        folium.Circle(
            location=(locations[i]["latitude"], locations[i]["longitude"]),
            radius=50000*((table[i]["total_precipitation"])/48), #Scales circle according to rainfall / precipitation
            tooltip=f"<h1>{table[i]["location"]}</h1>",
            popup=f"<h1>Precipitation: {table[i]["total_precipitation"]}</h1>",
            color='green',
            fill=True,
            fill_color='green',
        ).add_to(map)
    else:
        folium.Circle(
            location=(locations[i]["latitude"], locations[i]["longitude"]), #Non-standard precipitation
            radius=50000*((table[i]["total_precipitation"])/48), #Scales circle according to rainfall / precipitation
            tooltip=f"<h1>{table[i]["location"]}</h1>",
            popup=f"<h1>Precipitation: {table[i]["total_precipitation"]}</h1>",
            color='orange',
            fill=True,
            fill_color='orange',
        ).add_to(map)


map.save("map.html")
