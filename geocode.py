import sys
import logger
import pandas as pd
import config as cfg
from geopy.geocoders import GoogleV3
from unifier import unify


# API key stored off repo for security purposes (although it's not that dangerous)
API_KEY = cfg.API_KEY


def geolocate(data, column):
    # Setting up the geolocator to connect to Google's Geocoding API, biasing results to the UK by specifying the domain
    # timeout is to stop there being too many requests a second and making things difficult.
    geolocator = GoogleV3(api_key=API_KEY, domain="maps.google.co.uk", timeout=100)

    lat = []
    lon = []
    missing = []
    missing_count = 0
    count = 0

    # Loop grabs each library, extracts the useful address data and passes this to the Google API to return location data
    # Lat and Lon are then grabbed and stored.
    for _, row in data.iterrows():
        count += 1
        address = "{}".format(row[column])
        location = geolocator.geocode(address)

        if location is None:
            lat.append(None)
            lon.append(None)

            missing.append(address)
            missing_count += 1

        else:
            lat.append(location.latitude)
            lon.append(location.longitude)

        if (count % 25) == 0:
            print("Addresses processed: {}".format(count))

    data["LAT"] = lat
    data["LON"] = lon

    return data, missing


def run(input, column, columns):
    log = logger.get_logger("geoharm.py")
    log.info("Geocoding...")

    if (".xls" in input) or (".xlsx" in input):
        data = pd.read_excel("./data/{}".format(input))

    elif ".csv" in input:
        data = pd.read_csv("./data/{}".format(input))

    else:
        sys.exit("Cannot determine the filetype of input, is it .csv, .xls or .xlsx?")

    log.info("Dataset size: {}".format(len(data)))

    if columns is "":
        with open("./data/{}.txt".format(columns), "r") as myfile:
            columns = [line.split(", ") for line in myfile.readlines()][0]

        data = unify(data, columns)

    output, missing = geolocate(data, column)

    log.info("Number of missing geolocations: {}".format(len(missing)))

    input = input.split(".")[0]

    output.to_csv("./results/{}/{}_geo.csv".format(input, input))

    with open('./results/{}/{}_missing.txt'.format(input, input), mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(missing))

    log.info("Geolocating finished. Output saved to ./results/{}/".format(input))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filename (including extension) that contains addresses")
    parser.add_argument("column", help="Name of column where the address exists")
    parser.add_argument("--columns", help="File containing columns that you want to merge into one", required=False, default="")

    args = parser.parse_args()

    run(args.input, args.column, args.columns)
