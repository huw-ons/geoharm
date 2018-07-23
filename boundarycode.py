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

    geo_data["geometry"] = geo_data["geometry"].to_crs({"init": "epsg:4326"})

    return geo_data


def prepare_boundaries(boundaries, geo_data):
    boundaries.crs = geo_data.crs
    # Trying to put the boundaries into a compatible CRS with the datasets
    boundaries.crs = {"init": "epsg:3857"}
    boundaries["geometry"] = boundaries["geometry"].to_crs({"init": "epsg:3857"})

    return boundaries


def geomerge(geo_data, boundaries):
    boundary_data = gpd.sjoin(geo_data, boundaries, op="intersects", how="left")

    return boundary_data


def produce_map(geo_data, boundaries, output_name):
    fig, ax = plt.subplots(figsize=(20,20))
    ax.set_aspect("equal")

    geo_data.plot(ax=ax, markersize=50, color="red")
    boundaries.plot(ax=ax, color="none", edgecolor="black")
    plt.savefig("./maps/{}.png".format(output_name))


def produce_empty(geo_data, boundaries, boundary_data, output_name):
    # TODO Fix this up as it isn't catching empty boundaries
    missing = boundary_data[boundary_data.isnull()].index

    if len(missing) > 0:
        fig, ax = plt.subplots(figsize=(15,15))
        ax.set_aspect("equal")

        geo_data.plot(ax=ax, markersize=1.5, color="red")
        boundaries[boundaries["geo_code"].isin(missing)].plot(ax=ax, color="blue", edgecolor="black")
        plt.savefig("./maps/{}_missing.png".format(output_name))

    else:
        print("No boundaries that are empty, happy days! Not writting empty map file")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("data_input", help="Filename (not including extension) that contains coordinates")
    parser.add_argument("boundary_input", help="Filename (not including extension) of Shapefile")
    parser.add_argument("output", help="Filename (not including extension) to output merged file to")
    parser.add_argument("--map_output", help="Filename (not including extension) to write maps to", required=False, default=None)

    args = parser.parse_args()

    try:
        data = pd.read_csv("./results/{}.csv".format(args.data_input)).dropna(subset=["LAT", "LON"])
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

    boundaries = prepare_boundaries(boundaries, geo_data)
    print("Boundaries prepared")

    print("Beginning merge...")
    boundary_data = geomerge(geo_data, boundaries)
    print("Merge completed...")

    if args.map_output is not None:
        print("Outputting maps")
        produce_map(geo_data, boundaries, args.map_output)
        produce_empty(geo_data, boundaries, boundary_data, args.map_output)

    print("Writing merged dataset to file...")
    boundary_data.to_csv("./results/{}_boundary.csv".format(args.output))

    print("Done.")
