import folium
import pandas as pd

map_osm = folium.Map()

data = pd.read_csv("./results/geo_libraries.csv")

for _, row in data.iterrows():
    name = '{} {} {} {}'.format(row["TITLE"], row["STREET_ADDRESS"], row["TOWN"], row["POSTCODE"])
    popup = folium.Popup(name, parse_html=True)
    folium.Marker([row["LAT"], row["LON"]], popup=popup).add_to(map_osm)

map_osm.save("./maps/map.html")
