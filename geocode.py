from geopy.geocoders import GoogleV3
import pandas as pd

API_KEY = "AIzaSyAKCNAFKTpl3RqFBI2Qe799ZVdeyVUFbd8"

data = pd.read_excel("./data/libraries.xls")

geolocator = GoogleV3(api_key=API_KEY)

#location = geolocator.geocode("19 Cefn Parc Tredegar NP223PH Wales")

subset = data.head(10)

lat = []
lon = []
missing = 0

for _, row in subset.iterrows():
    address = "{}, {}, {}, {}".format(row["TITLE"], row["STREET_ADDRESS"], row["TOWN"], row["POSTCODE"])
    location = geolocator.geocode(address)

    if location is None:
        print("Cannot find location for {}".format(address))
        missing += 1

    else:
        lon.append(location.longitude)
        lat.append(location.latitude)

print("Number of missing addresses: {}".format(missing))

subset["LON"] = lon
subset["LAT"] = lat

subset.to_csv("test.csv")