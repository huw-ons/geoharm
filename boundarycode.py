import os
import sys
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point


def prepare_dataset(data):
    # Converts Lon and Lat columns into geometry Point objects for geopandas
    geometry = [Point(xy) for xy in zip(data.LON, data.LAT)]

    # This is the CRS that seems to best fit as found by QGIS
    crs = {"init": "epsg:4326"}
    geo_data = gpd.GeoDataFrame(data, crs=crs, geometry=geometry)
    geo_data = geo_data.to_crs({"init": "epsg:3857"})

    return geo_data


def prepare_boundaries(boundaries):
    boundaries = boundaries.to_crs({"init": "epsg:3857"})

    return boundaries


def geomerge(geo_data, boundaries):
    boundary_data = gpd.sjoin(geo_data, boundaries, op="within", how="right")

    return boundary_data


def remove_missing(geo_data, boundary_data, boundaries):
    boundary_data = boundary_data.dropna(subset=["ADDRESS"])
    geo_data = geo_data[geo_data["ADDRESS"].isin(boundary_data["ADDRESS"])]
    missing_boundaries = boundaries[~boundaries["geo_code"].isin(boundary_data["geo_code"])]
    filled = len(boundaries) - len(missing_boundaries)

    print("There are {} boundaries with a data point out of {}".format(filled, len(boundaries)))

    return geo_data, boundary_data


def produce_empty(geo_data, boundaries, boundary_data, boundary_name, output_name):
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_aspect("equal")

    boundary_data.plot(ax=ax, color="none", edgecolor="black")
    boundaries[~boundaries["geo_code"].isin(boundary_data["geo_code"])].plot(ax=ax, color="blue", edgecolor="black")
    geo_data.plot(ax=ax, markersize=0.5, color="red")
    check_folder("./maps/{}/{}/".format(output_name, boundary_name))
    plt.savefig("./maps/{}/{}/{}_missing.png".format(output_name, boundary_name, output_name))


def check_folder(path):
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data_input", help="Filename (not including extension) that contains coordinates")
    parser.add_argument("boundary_input", help="Filename (not including extension) of Shapefile")
    parser.add_argument("--map_output", help="Flag to specify whether to write debugging maps", required=False, default="N")

    args = parser.parse_args()
    stripped_input = args.data_input.split("_")[0]

    try:
        data = pd.read_csv("./results/{}/{}_geo.csv".format(stripped_input, stripped_input)).dropna(subset=["LAT", "LON"])
    except FileNotFoundError:
        sys.exit("Cannot find data file, exiting")

    print("Data file loaded")

    try:
        boundaries = gpd.read_file("./data/boundaries/{}.shp".format(args.boundary_input))
    except FileNotFoundError:
        sys.exit("Cannot find boundary file, exiting")

    print("Boundary file loaded")

    geo_data = prepare_dataset(data)
    print("Data prepared")

    boundaries = prepare_boundaries(boundaries)
    print("Boundaries prepared")

    print("Beginning merge...")
    boundary_data = geomerge(geo_data, boundaries)
    print("Merge completed...")

    print("Cleaning up...")
    geo_data, boundary_data = remove_missing(geo_data, boundary_data, boundaries)

    if args.map_output is "Y":
        print("Outputting maps")
        produce_empty(geo_data, boundaries, boundary_data, args.boundary_input, stripped_input)

    print("Writing merged dataset to file...")
    check_folder("./results/{}/{}/".format(stripped_input, args.boundary_input))
    boundary_data.to_csv("./results/{}/{}/{}_boundaries.csv".format(stripped_input, args.boundary_input, stripped_input))

    print("Done.")
