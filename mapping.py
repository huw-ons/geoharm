import sys
import folium
import numpy as np
import pandas as pd
from folium.plugins import MarkerCluster


def create_map(data, output, name=None):
    print("Beginning mapping...")

    map_osm = folium.Map()

    marker_cluster = MarkerCluster().add_to(map_osm)

    for _, row in data.iterrows():
        # Filters out any addresses that coordinates could not be obtained for
        if not np.isnan(row["LAT"]) and not np.isnan(row["LON"]):
            if name is not None:
                popup = folium.Popup(row[name], parse_html=True)
                folium.Marker([row["LAT"], row["LON"]], popup=popup).add_to(marker_cluster)
            else:
                folium.Marker([row["LAT"], row["LON"]]).add_to(marker_cluster)

    map_osm.save("./maps/{}/{}_map.html".format(output, output))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filename (not including extension, must be csv) that has coordinates")
    parser.add_argument("--name", help="Column name of address if want to include as a popup", required=False, default=None)

    args = parser.parse_args()
    stripped_input = args.input.split("_")[0]

    try:
        data = pd.read_csv("./results/{}/{}.csv".format(stripped_input, args.input))
    except FileNotFoundError:
        sys.exit("Cannot find data file, exiting")

    create_map(data, stripped_input, args.name)

    print("Mapping finished. Output saved to ./maps/{}/".format(stripped_input))
