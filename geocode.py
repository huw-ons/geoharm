from geopy.geocoders import GoogleV3
import pandas as pd
import config as cfg

# API key stored off repo for security purposes (although it's not that dangerous)
API_KEY = cfg.API_KEY

data = pd.read_excel("./data/libraries.xls")

# Setting up the geolocator to connect to Google's Geocoding API, biasing results to the UK by specifying the domain,
# timeout is to stop there being too many requests a second and making things difficult.
geolocator = GoogleV3(api_key=API_KEY, domain="maps.google.co.uk", timeout=100)

lat = []
lon = []
missing = 0
count = 0

# Loop grabs each library, extracts the useful address data and passes this to the Google API to return location data
# Lat and Lon are then grabbed and stored.
# TODO Get the whole location raw dump and save that elsewhere? Just in case we want to investigate anything else
for _, row in data.iterrows():
    count += 1
    address = "{}, {}, {}, {}".format(row["TITLE"], row["STREET_ADDRESS"], row["TOWN"], row["POSTCODE"])
    location = geolocator.geocode(address)

    if location is None:
        print("Cannot find location for {}".format(address))
        missing += 1

    else:
        lat.append(location.latitude)
        lon.append(location.longitude)

    if (count % 25) == 0:
        print("Addresses processed: {}".format(count))

print("Number of missing addresses: {}".format(missing))

data["LAT"] = lat
data["LON"] = lon

data.to_csv("./results/geo_libraries.csv")
