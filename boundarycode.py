import os
import sys
import logger
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
    # Matching the boundary CRS to the data CRS
    boundaries = boundaries.to_crs({"init": "epsg:3857"})

    return boundaries


def geomerge(geo_data, boundaries):
    boundary_data = gpd.sjoin(geo_data, boundaries, op="within", how="right")

    return boundary_data


def remove_missing(geo_data, boundary_data, boundaries):
    # Dropping all rows without an address, an indication that there was nothing to merge with
    boundary_data = boundary_data.dropna(subset=["ADDRESS"])
    geo_data_uk = geo_data[geo_data["ADDRESS"].isin(boundary_data["ADDRESS"])]
    outside_uk = len(geo_data) - len(geo_data_uk)
    missing_boundaries = boundaries[~boundaries["geo_code"].isin(boundary_data["geo_code"])]
    filled = len(boundaries) - len(missing_boundaries)

    return geo_data_uk, boundary_data, filled, outside_uk


def produce_map(geo_data, boundaries, boundary_data, boundary_name, output_name):
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


def run(data_input, boundary_input, map_output):
    log = logger.get_logger("boundarycode.py")
    log.info("Boundary coding...")
    log.info("Boundary used: {}".format(boundary_input))

    stripped_input = data_input.split("_")[0]

    try:
        data = pd.read_csv("./results/{}/{}_geo.csv".format(stripped_input, stripped_input)).dropna(
            subset=["LAT", "LON"])
    except FileNotFoundError:
        sys.exit("Cannot find data file, exiting")

    log.info("Data file loaded")

    try:
        boundaries = gpd.read_file("./data/boundaries/{}.shp".format(boundary_input))
    except FileNotFoundError:
        sys.exit("Cannot find boundary file, exiting")

    log.info("Boundary file loaded")

    geo_data = prepare_dataset(data)
    log.info("Data prepared")

    boundaries = prepare_boundaries(boundaries)
    log.info("Boundaries prepared")

    log.info("Number of boundaries: {}".format(len(boundaries)))

    log.info("Beginning merge...")
    boundary_data = geomerge(geo_data, boundaries)
    log.info("Merge completed...")

    log.info("Cleaning up...")
    geo_data, boundary_data, filled, outside_uk = remove_missing(geo_data, boundary_data, boundaries)

    log.info("Filled boundaries: {}".format(filled))
    log.info("Number of locations outside UK: {}".format(outside_uk))

    if map_output is "Y":
        log.info("Outputting maps")
        produce_map(geo_data, boundaries, boundary_data, boundary_input, stripped_input)

    check_folder("./results/{}/{}/".format(stripped_input, boundary_input))
    boundary_data.to_csv("./results/{}/{}/{}_boundaries.csv".format(stripped_input, boundary_input, stripped_input))
    log.info("Boundary coding finished. Output saved to ./results/{}/{}/{}_boundaries.csv".format(stripped_input, boundary_input, stripped_input))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data_input", help="Filename (not including extension) that contains coordinates")
    parser.add_argument("boundary_input", help="Filename (not including extension) of Shapefile")
    parser.add_argument("--map_output", help="Flag to specify whether to write debugging maps", required=False, default="N")

    args = parser.parse_args()

    run(args.data_input, args.boundary_input, args.map_output)