from geopy.geocoders import GoogleV3
import pandas as pd
import config as cfg

API_KEY = cfg.API_KEY

data = pd.read_excel("./data/libraries.xls")

geolocator = GoogleV3(api_key=API_KEY)

subset = data.head(10)

lat = []
lon = []
missing = 0

for _, row in data.iterrows():
    address = "{}, {}, {}, {}".format(row["TITLE"], row["STREET_ADDRESS"], row["TOWN"], row["POSTCODE"])
    location = geolocator.geocode(address)

    if location is None:
        print("Cannot find location for {}".format(address))
        missing += 1

    else:
        lat.append(location.latitude)
        lon.append(location.longitude)

print("Number of missing addresses: {}".format(missing))

data["LAT"] = lat
data["LON"] = lon

data.to_csv("./results/geo_libraries.csv")
