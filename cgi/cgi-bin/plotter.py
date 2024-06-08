import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

def get_standard_time(time):
    return f"{time//60}:{time%60:02d}"

def plot_graph(G, cities, full_path, filepath):
    pos = {city: (data["long"], data["lat"]) for city, data in G.nodes(data=True)}

    # add background map
    world = gpd.read_file("./cgi-bin/static/map/ne_110m_admin_0_countries.shp")
    ax = world.plot(figsize=(20, 16))
    ax.set_xlim(-11, 34)
    ax.set_ylim(35.8, 70)

    # color edges blue if they are a ferry & red if they are a reservation
    edge_colors = [
        "blue" if data["type"] == "ferry" 
        else "red" if data["type"] == "reservation" 
        else "black" for u, v, data in G.edges(data=True)]

    nx.draw(G, pos, node_size=40, font_size=9, node_color='red', edge_color=edge_colors, ax=ax)

    # highlight full_path in the plot and node labels for visited cities
    edges = [(full_path[i], full_path[i+1]) for i in range(len(full_path)-1)]
    edge_labels = {edge : get_standard_time(G.edges[edge]["time"]) for edge in edges}

    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="pink", width=2, ax=ax)
    nx.draw_networkx_edge_labels(G, pos, font_size=7, ax=ax, edge_labels=edge_labels)

    node_labels = {node: node for node in cities}
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=13, ax=ax,verticalalignment='top')
    nx.draw_networkx_nodes(G, pos, nodelist = cities,node_size=60, node_color='yellow', ax=ax)

    plt.savefig(filepath, format="png", bbox_inches='tight')
