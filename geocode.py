import sys
import pandas as pd
import config as cfg
from geopy.geocoders import GoogleV3
from unifier import unify


# API key stored off repo for security purposes (although it's not that dangerous)
API_KEY = cfg.API_KEY


def geolocate(data, column):
    # Setting up the geolocator to connect to Google's Geocoding API, biasing results to the UK by specifying the domain
    # timeout is to stop there being too many requests a second and making things difficult.

    print("Beginning geolocator")

    geolocator = GoogleV3(api_key=API_KEY, domain="maps.google.co.uk", timeout=100)

    lat = []
    lon = []
    missing = []
    missing_count = 0
    count = 0

    # Loop grabs each library, extracts the useful address data and passes this to the Google API to return location data
    # Lat and Lon are then grabbed and stored.
    # TODO Get the whole location raw dump and save that elsewhere? Just in case we want to investigate anything else
    for _, row in data.iterrows():
        count += 1
        address = "{}".format(row[column])
        location = geolocator.geocode(address)

        if location is None:
            print("Cannot find location for {}".format(address))

            lat.append(None)
            lon.append(None)

            missing.append(address)
            missing_count += 1

        else:
            # TODO Do a better job of catching addresses outside the UK
            lat.append(location.latitude)
            lon.append(location.longitude)

        if (count % 25) == 0:
            print("Addresses processed: {}".format(count))

    print("Number of missing addresses: {}".format(missing_count))

    data["LAT"] = lat
    data["LON"] = lon

    return data, missing


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filename (including extension) that contains addresses")
    parser.add_argument("output", help="Filename (including extension) that output is written to")
    parser.add_argument("column", help="Name of column where the address exists")
    parser.add_argument("--columns", help="File containing columns that you want to merge into one", required=False)

    args = parser.parse_args()

    if (".xls" in args.input) or (".xlsx" in args.input):
        data = pd.read_excel("./data/{}".format(args.input))

    elif ".csv" in args.input:
        data = pd.read_csv("./data/{}".format(args.input))

    else:
        sys.exit("Cannot determine the filetype of input, is it .csv, .xls or .xlsx?")

    if args.columns:
        with open("./data/{}.txt".format(args.columns), "r") as myfile:
            columns = [line.split(", ") for line in myfile.readlines()][0]

        data = unify(data, columns)

    output, missing = geolocate(data, args.column)

    output.to_csv("./results/{}".format(args.output))

    with open('./results/{}_missing'.format(args.output), mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(missing))

    print("Geolocating finished. Output saved to ./results/{}".format(args.output))
