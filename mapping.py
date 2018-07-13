import sys
import folium
import pandas as pd
from folium.plugins import MarkerCluster


def create_map(data, output, name):
    map_osm = folium.Map()

    marker_cluster = MarkerCluster().add_to(map_osm)

    for _, row in data.iterrows():
        popup = folium.Popup(name, parse_html=True)
        folium.Marker([row["LAT"], row["LON"]], popup=popup).add_to(marker_cluster)

    map_osm.save("./maps/{}.html".format(output))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Filename (including extension, must be csv) that has coordinates")
    parser.add_argument("output", help="Filename (not including extension) for output file")
    parser.add_argument("name", help="Column name of address if want to include as a popup")

    args = parser.parse_args()

    if ".csv" in args.input:
        data = pd.read_csv("./data/{}".format(args.input))

    else:
        sys.exit("Cannot determine the filetype of input, is it a .csv?")

    create_map(data, args.output, args.name)

    print("Mapping finished. Output saved to ./maps/{}.html".format(args.output))
