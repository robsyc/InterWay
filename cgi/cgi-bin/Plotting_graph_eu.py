import cgi, cgitb
from geopy.geocoders import Nominatim
from geopy import distance
import pandas as pd
import networkx as nx
import pickle
from networkx.utils import open_file
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as cx
import random


cities = ["Westport","Belfast","Dublin","Cork","Aberdeen","Glasgow","Edinburgh","York","London","Holyhead","Birmingham","Bristol","Penzance","Brussels","Amsterdam","Paris","Rennes","Lyon","Bordeaux","Montpellier","Hendaye","Marseille","Nice","Madrid","Barcelona","Valencia","Pamplona","Santander","Santiago","Sevilla","Vigo", "Granada", "Malaga","Lisbon","Porto","Faro","Rome", "Milan", "Genova", "Bologna", "Firenze", "Napoli","Bari", "Catania", "Venezia","Zurich","Basel","Bern","Köln","Hamburg", "Berlin", "München", "Frankfurt", "Praha","Copenhagen","Aarhus","Stockholm","Kiruna","Östersund","Oslo","Bergen","Trondheim","Bodø","Helsinki","Turku","Rovaniemi","Tallinn","Narva", "Tartu", "Viljandi", "Valga","Riga","Daugavpils","Liepaja","Vilnius","Kaunas","Klaipeda","Trakai","Warsaw","Krakow","Gdansk","Katowice","Przemysl","Poznan","Wien","Ljubljana","Zagreb","Split","Budapest","Belgrade","Bar","Skopje","Bucharest", "Cluj-Napoca", "Craiova","София", "Варна","Αθήνα", "Θεσσαλονίκη", "Πάτρα","Istanbul", "Ankara", "Eskisehir", "Konya"]

rails = [
    ("Cork", "Dublin", 165),
    ("Dublin", "Belfast", 130),
    ("Dublin", "Westport", 190),

    ("Dublin", "Holyhead", 195, "ferry"),

    ("Aberdeen", "Edinburgh", 140),
    ("Edinburgh", "Glasgow", 50),
    ("Edinburgh", "York", 155,"reservation"),
    ("Edinburgh", "Birmingham", 260),
    ("Glasgow", "Birmingham", 290,"reservation"),
    ("Holyhead", "London", 230),
    ("Birmingham", "London", 85,"reservation"),
    ("York", "London", 110,"reservation"),
    ("Bristol", "London", 95,"reservation"),
    ("Penzance", "London", 305,"reservation"),

    ("London", "Brussels", 155,"reservation"),
    ("London", "Paris", 170,"reservation"),
    ("Brussels", "Paris", 85,"reservation"),

    ("Paris", "Rennes", 130,"reservation"),
    ("Paris", "Bordeaux", 195,"reservation"),
    ("Bordeaux", "Lyon", 375),
    ("Montpellier", "Marseille", 115,"reservation"),
    ("Marseille", "Nice", 155,"reservation"),
    ("Lyon", "Marseille", 100,"reservation"),
    ("Bordeaux", "Hendaye", 180),

    ("Paris", "Barcelona", 390,"reservation"),
    ("Montpellier", "Barcelona", 180,"reservation"),
    ("Hendaye", "Madrid", 380),

    ("Madrid", "Barcelona", 150,"reservation"),
    ("Madrid", "Pamplona", 180,"reservation"),
    ("Madrid", "Santander", 270,"reservation"),
    ("Madrid", "Santiago", 310,"reservation"),
    ("Madrid", "Valencia", 100,"reservation"),
    ("Madrid", "Sevilla", 140,"reservation"),
    ("Madrid", "Malaga", 145,"reservation"),
    ("Madrid", "Granada", 195,"reservation"),
    ("Barcelona", "Valencia", 190,"reservation"),
    ("Barcelona", "Sevilla", 330,"reservation"),
    ("Santiago", "Vigo", 90,"reservation"),

    ("Vigo", "Porto", 140,"reservation"),
    ("Porto", "Lisbon", 160,"reservation"),
    ("Lisbon", "Faro", 180,"reservation"),

    ("Nice", "Genova", 295,"reservation"),
    ("Lyon", "Bern", 230),
    ("Paris", "Basel", 185,"reservation"),
    ("Paris", "Frankfurt", 235,"reservation"),

    ("Bern", "Zurich", 56),
    ("Basel", "Bern", 58),
    ("Basel", "Frankfurt", 165),

    ("Bern", "Milan", 180,"reservation"),
    ("Zurich", "Milan", 195,"reservation"),
    ("Milan", "Genova", 98,"reservation"),
    ("Milan", "Venezia", 155,"reservation"),
    ("Milan", "Bologna", 60,"reservation"),
    ("Bologna", "Firenze", 35,"reservation"),
    ("Bologna", "Bari", 320,"reservation"),
    ("Firenze", "Rome", 90,"reservation"),
    ("Rome", "Genova", 245,"reservation"),
    ("Rome", "Napoli", 65,"reservation"),
    ("Rome", "Bari", 240,"reservation"),
    ("Catania", "Napoli", 450,"reservation"),

    ("Venezia", "Ljubljana", 390),
    ("Venezia", "München", 450),
    ("Venezia", "Wien", 460),
    ("Milan", "München", 450),
    ("Wien", "München", 240),
    ("Wien", "Zurich", 600),

    ("München", "Zurich", 210),
    ("München", "Frankfurt", 200),
    ("München", "Berlin", 270),
    ("München", "Hamburg", 360),
    ("München", "Praha", 360),
    ("Berlin", "Praha", 245),
    ("Berlin", "Hamburg", 100),
    ("Berlin", "Köln", 260),
    ("Berlin", "Frankfurt", 235),
    ("Amsterdam", "Köln", 158),
    ("Brussels", "Köln", 110),
    ("Frankfurt", "Köln", 65),
    ("Frankfurt", "Hamburg", 220),
    ("Frankfurt", "Brussels", 190),

    ("Amsterdam", "Brussels", 110,"reservation"),
    ("Amsterdam", "Hamburg", 315),

    ("Wien", "Ljubljana", 360),
    ("Wien", "Praha", 240),
    ("Wien", "Budapest", 160),
    ("Praha", "Budapest", 405),
    ("Ljubljana", "Zagreb", 140,"reservation"),
    ("Ljubljana", "Budapest", 585),
    ("Zagreb", "Split", 360,"reservation"),
    ("Zagreb", "Budapest", 400,"reservation"),

    ("Hamburg", "Aarhus", 265,"reservation"),
    ("Hamburg", "Copenhagen", 280,"reservation"),

    ("Stockholm", "Copenhagen", 300,"reservation"),
    ("Oslo", "Copenhagen", 450),
    ("Oslo", "Stockholm", 360),
    ("Oslo", "Bergen", 405,"reservation"),
    ("Oslo", "Trondheim", 390,"reservation"),
    ("Trondheim", "Bodø", 570,"reservation"),
    ("Östersund", "Trondheim", 220),
    ("Östersund", "Stockholm", 305,"reservation"),
    ("Stockholm", "Kiruna", 975,"reservation"),

    ("Rovaniemi", "Helsinki", 510),
    ("Turku", "Helsinki", 120),

    ("Tallinn", "Stockholm", 960, "ferry"),
    ("Tallinn", "Helsinki", 120, "ferry"),
    ("Stockholm", "Riga", 1020, "ferry"),


    ("Tallinn", "Narva", 135),
    ("Tallinn", "Viljandi", 115),
    ("Tallinn", "Tartu", 115),
    ("Tartu", "Valga", 80),

    ("Valga", "Riga", 260),
    ("Riga", "Liepaja", 67),
    ("Riga", "Daugavpils", 200),

    ("Vilnius", "Klaipeda", 240,"reservation"),
    ("Vilnius", "Kaunas", 80,"reservation"),
    ("Vilnius", "Trakai", 240,"reservation"),

    ("Warsaw", "Gdansk", 160,"reservation"),
    ("Warsaw", "Poznan", 180,"reservation"),
    ("Warsaw", "Katowice", 130,"reservation"),
    ("Warsaw", "Krakow", 130,"reservation"),
    ("Berlin", "Poznan", 165,"reservation"),
    ("Berlin", "Katowice", 365,"reservation"),
    ("Krakow", "Katowice", 65,"reservation"),
    ("Krakow", "Przemysl", 190,"reservation"),
    ("Katowice", "Praha", 320,"reservation"),
    ("Katowice", "Wien", 268),

    ("Budapest", "Cluj-Napoca", 400),
    ("Budapest", "Bucharest", 900,"reservation"),
    ("Budapest", "Craiova", 660,"reservation"),
    ("Budapest", "Belgrade", 485,"reservation"),

    ("Bucharest", "Cluj-Napoca", 570,"reservation"),
    ("Bucharest", "Craiova", 400,"reservation"),
    ("Bucharest", "Варна", 525,"reservation"),
    ("Bucharest", "София", 565),

    ("София", "Craiova", 510),
    ("София", "Belgrade", 530,"reservation"),
    ("София", "Istanbul", 580,"reservation"),
    ("София", "Θεσσαλονίκη", 440,"reservation"),

    ("Belgrade", "Skopje", 590),
    ("Belgrade", "Bar", 500,"reservation"),

    ("Skopje", "Θεσσαλονίκη", 300),
    ("Αθήνα", "Θεσσαλονίκη", 263,"reservation"),
    ("Αθήνα", "Πάτρα", 180,"reservation"),

    ("Istanbul", "Eskisehir", 150,"reservation"),
    ("Ankara", "Eskisehir", 90,"reservation"),
    ("Ankara", "Konya", 110,"reservation"),

    ("Πάτρα", "Bari", 930, "ferry"),
    ("Barcelona", "Genova", 1020, "ferry"),
    ("Belfast", "Glasgow", 195, "ferry")
]


# Getting coordinates of cities and calculate distances
geolocator = Nominatim(user_agent="robbe.claeys@gmail.com")

def limit_locations_EU(locations):
    lat_min, lat_max = 35.8, 72
    long_min, long_max = -11, 36
    return [location for location in locations if lat_min <= location.latitude <= lat_max and long_min <= location.longitude <= long_max][0]

def get_country_long_lat(city):
    locations = geolocator.geocode(city, exactly_one=False)
    # print(locations)
    if len(locations) > 1:
        location = limit_locations_EU(locations)
        # print(location)
    else:
        location = locations[0]
    country = location.address.split(",")[-1].strip()
    return (country, location.latitude, location.longitude)

def get_distance(geo1, geo2):
    return distance.distance(geo1, geo2).km



#Create graph of EU
try:
    # open local graph
    @open_file(0, mode="rb")
    def pickle_load(path):
        return pickle.load(path)

    G = pickle_load("./data/cities.gpickle")


except:
    # create new graph
    G = nx.Graph()

    for city in cities:
        print(city)
        country, lat, long = get_country_long_lat(city)
        #airport_code = get_airport(lat, long)

        G.add_node(
            city,                       # node name
            country=country,            # country
            lat=lat,                    # latitude
            long=long,                  # longitude
            #iata_code=airport_code,     # airport code
            weight=1                    # weight (desire to visit)
            )

    # save networkx graph locally (avoid API calls to Nominatim geocoder)
    @open_file(1, mode="wb")
    def write_gpickle(G, path, protocol=pickle.HIGHEST_PROTOCOL):
        pickle.dump(G, path, protocol)

    write_gpickle(G, "./data/cities.gpickle")


#Adding edges (railway connections) to the graph
for rail in rails:
    #print(rail)
    node1 = G.nodes[rail[0]]
    geo1 = (node1['lat'], node1['long'])
    node2 = G.nodes[rail[1]]
    geo2 = (node2['lat'], node2['long'])

    dist = get_distance(geo1, geo2)

    if rail[-1] == "ferry":
        rail_type = "ferry"
    elif rail[-1] == "reservation":
        rail_type = "reservation"
    else:
        rail_type = "rail"
    
    G.add_edge(
        rail[0], rail[1],
        distance=dist,
        time=rail[2],
        type=rail_type
    )


# Plot graph
# plot graph using longitude and latitude features of nodes as x and y coordinates

def plot_graph_all_labels(G, paths=None, weight="time", figsize=(20, 16)):
    pos = {city: (data["long"], data["lat"]) for city, data in G.nodes(data=True)}

    # add background map
    # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = gpd.read_file("./data/map/ne_110m_admin_0_countries.shp")
    ax = world.plot(figsize=(20, 16))
    ax.set_xlim(-11, 34)
    ax.set_ylim(35.8, 70)

    # color nodes grey if they have no airport "iata_code"
    #node_colors = ["red" if data["iata_code"] else "grey" for city, data in G.nodes(data=True)]

    # color edges blue if they are a ferry & red if they are a reservation
    edge_colors = [
        "blue" if data["type"] == "ferry" 
        else "red" if data["type"] == "reservation" 
        else "black" for u, v, data in G.edges(data=True)]

    # add edge feature "time" in format hh:mm to the plot
    edge_labels = {(u, v): f"{data['time']//60}:{data['time']%60:02d}" for u, v, data in G.edges(data=True)}

    
    nx.draw(G, pos, with_labels=True, node_size=40, font_size=9, node_color='red', edge_color=edge_colors, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)


    # add paths to the plot
    if paths:
        for path in paths:
            edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="pink", width=2, ax=ax)

    #save as jpg with very high resolution
    plt.savefig("./data/eu_map_path.svg", dpi=300)
    #plt.savefig("./data/eu_map_path1.jpeg")








def plot_graph(G, cities, full_path, weight="time", figsize=(20, 16)):
    pos = {city: (data["long"], data["lat"]) for city, data in G.nodes(data=True)}

    # add background map
    # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = gpd.read_file("./data/map/ne_110m_admin_0_countries.shp")
    ax = world.plot(figsize=(20, 16))
    ax.set_xlim(-11, 34)
    ax.set_ylim(35.8, 70)

    # color nodes grey if they have no airport "iata_code"
    #node_colors = ["red" if data["iata_code"] else "grey" for city, data in G.nodes(data=True)]

    # color edges blue if they are a ferry & red if they are a reservation
    edge_colors = [
        "blue" if data["type"] == "ferry" 
        else "red" if data["type"] == "reservation" 
        else "black" for u, v, data in G.edges(data=True)]

    nx.draw(G, pos, node_size=40, font_size=9, node_color='red', edge_color=edge_colors, ax=ax)

    # Highlight full_path in the plot and node labels for visited cities
    if full_path:
        for path in full_path:
            edges = list(zip(path, path[1:]))
            edge_labels = {(u, v): f"{data['time']//60}:{data['time']%60:02d}" for u, v, data in G.edges(data=True) if u in path and v in path}
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="pink", width=2, ax=ax)
            nx.draw_networkx_edge_labels(G, pos, font_size=7, ax=ax,edge_labels=edge_labels)

    node_labels = {node: node for node in cities}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=13, ax=ax,verticalalignment='top')
    nx.draw_networkx_nodes(G, pos, nodelist = cities,node_size=60, node_color='yellow', ax=ax)

    plt.savefig("./data/eu_map_path.svg", dpi=300)




path = ['Brussels', 'Köln', 'Berlin', 'Katowice', 'Krakow', 'Katowice', 'Wien', 'Budapest', 'Belgrade']
cities = ['Brussels', 'Berlin', 'Krakow', 'Wien', 'Budapest', 'Belgrade']
plot_graph(G,full_path=[path], cities = cities)

