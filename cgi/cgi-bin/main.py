#!/usr/bin/env python3
import cgi, cgitb
import pickle
import networkx as nx
from networkx.utils import open_file

from optimizer import get_paths
from plotter import plot_graph
import os
import sys

# python -m http.server --cgi (Run in command line)
# Open http://localhost:8000/ 

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

########################################################################################################

cities = ["Westport","Belfast","Dublin","Cork","Aberdeen","Glasgow","Edinburgh","York","London","Holyhead","Birmingham","Bristol","Penzance","Brussels","Amsterdam","Paris","Rennes","Lyon","Bordeaux","Montpellier","Hendaye","Marseille","Nice","Madrid","Barcelona","Valencia","Pamplona","Santander","Santiago","Sevilla","Vigo", "Granada", "Malaga","Lisbon","Porto","Faro","Rome", "Milan", "Genova", "Bologna", "Firenze", "Napoli","Bari", "Catania", "Venezia","Zurich","Basel","Bern","Köln","Hamburg", "Berlin", "München", "Frankfurt", "Praha","Copenhagen","Aarhus","Stockholm","Kiruna","Östersund","Oslo","Bergen","Trondheim","Bodø","Helsinki","Turku","Rovaniemi","Tallinn","Narva", "Tartu", "Viljandi", "Valga","Riga","Daugavpils","Liepaja","Vilnius","Kaunas","Klaipeda","Trakai","Warsaw","Krakow","Gdansk","Katowice","Przemysl","Poznan","Wien","Ljubljana","Zagreb","Split","Budapest","Belgrade","Bar","Skopje","Bucharest", "Cluj-Napoca", "Craiova","София", "Варна","Αθήνα", "Θεσσαλονίκη", "Πάτρα","Istanbul", "Ankara", "Eskisehir", "Konya"]

# load networkx graph locally
@open_file(0, mode="rb")
def pickle_load(path):
    return pickle.load(path)

G = pickle_load("./cgi-bin/static/graph.gpickle")

########################################################################################################

# Get the form data
cgitb.enable()
print("Content-Type: text/html; charset=utf-8\n")
form = cgi.FieldStorage()

travel_day_max_time = 9 * 60
start, end = str(form.getvalue('start')), str(form.getvalue('end'))
traveldays = int(form.getvalue('traveldays'))
days = int(form.getvalue('days_to_reach'))

city_weights_user = dict()
for city in cities:
    assert (form.getvalue(city+"_extra") is not None, f"Extra weight for {city} not found!")
    if form.getvalue(city) is not None:
        city_weights_user[city] = max(float(form.getvalue(city)), float(form.getvalue(city+"_extra")))
    else:
        city_weights_user[city] = float(form.getvalue(city+"_extra"))

# Add "score" feature to nodes
for city, data in G.nodes(data=True):
    if city in city_weights_user:
        G.nodes[city]["score"] = city_weights_user[city]
    elif city == start:
        G.nodes[city]["score"] = 0
    else:
        G.nodes[city]["score"] = 1

########################################################################################################

# Generate results
result = get_paths(G, start, end, total_travel_days=days, travel_days=traveldays, travel_day_max_time=travel_day_max_time)

if result:
    num_results = min(3, len(result))
    result = sorted(result, key=lambda x: x["score"], reverse=True)

    for i, item in enumerate(result[:num_results]):
        stop_cities = item["path"]
        stop_days = item["stop_days"]
        full_paths = item["full_path"]
        score = item["score"]
        img_path = f"./web-page_extras/plots/plot{i}.png"
        plot_graph(G, stop_cities, full_paths, img_path)

########################################################################################################

# print("Content-Type: text/html; charset=utf-8\n")

# Display the results
print(f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>InterWay</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.min.js" integrity="sha384-BBtl+eGJRgqQAUMxJ7pMwbEyER4l1g+O15P+16Ep7Q9Q+zqX6gSbd85u4mG4QzX+" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="../web-page_extras/style.css">

    </head>

    <body>
        <div class="container">
            <h1>InterWay</h1>
            <p class="lead">Mathematically optimize your Interrail trip!</p>
            <hr>
""")
if result:
    print(f"""
            <div class="container">
                <h2>Parameters</h2>
                <div class="row">
                    <div class="col-md-6">
                        <div class="autocomplete form-group">
                            <label class="fw-bold" for="start">Start City:</label>
                            <input type="text" class="form-control" id="start" name="start" value="{start}">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="autocomplete form-group">
                            <label class="fw-bold" for="end">Destination city:</label>
                            <input type="text" class="form-control" id="end" name="end" value="{end}">
                        </div>
                    </div>
                </div>

                <br>

                <div class="row">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold" for="traveldays">Number of Interrail traveldays:</label>
                            <br>
                            <div class="form-check form-check-inline">
                                <input class="form-check-input" type="radio" name="traveldays" id="inlineRadio_{traveldays}" value="{traveldays}">
                                <label class="form-check-label" for="inlineRadio_{traveldays}">{traveldays}</label>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="fw-bold" for="days_to_reach">Number of days to reach destination city:</label>
                            <input type="number" class="form-control" id="days_to_reach" name="days_to_reach" min="0" value="{days}">
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="container">
                <h2>Resulting paths</h2>
                <div class="accordion" id="accordion">
    """)
    # bootstrap accordion
    for i, item in enumerate(result[:num_results]):
        cities = list(item["path"])
        stops = item["stop_days"]
        path = item["full_path"]
        score = item["score"]

        cities_copy = cities[1:-1].copy()
        stops_copy = stops.copy()
        city_list = []
        stop_list = []
        for stop in path[1:-1]:
            if stop == cities_copy[0]:
                city_list.append(cities_copy.pop(0))
                stop_list.append(stops.pop(0))
            else:
                city_list.append(stop)
                stop_list.append(0)

        print(f"""
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="heading{i}">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{i}" aria-expanded="true" aria-controls="collapse{i}">
                                    <div>
                                        <div>Score: {round(score)}</div>
                                        <br>
                                        <div style="font-weight:bold">{" → ".join(cities)}</div>
                                    </div>
                                </button>
                            </h2>
                            <div id="collapse{i}" class="accordion-collapse collapse" aria-labelledby="heading{i}" data-bs-parent="#accordion{i}">
                                <div class="accordion-body">
                                    <div class="table-responsive">
                                    <table class="table">
                                        <tr>
                                            <th>City</th>
                                            {"".join(f"<th><u>{city}</u></th>" if stop_list[j] != 0 else f"<th>{city}</th>" for j, city in enumerate(city_list))}
                                        </tr>
                                        <tr>
                                            <th>Days spent</th>
                                            {"".join(f"<td>{stop}</td>" if stop!=0 else "<td></td>" for stop in stop_list)}
                                        </tr>
                                    </table>
                                    </div>
                                    <img src="../web-page_extras/plots/plot{i}.png" class="img-fluid" alt="plot{i}">
                                </div>
                            </div>
                        </div>
    """.format(encoding="utf-8"))
    print(f"""
                </div>
            </div>  
        </div>
    """)
else:
    print(f"""
            <div class="container">
                <h2>No results :(</h2>
                <p>No valid paths found. Please try again with more Interrail traveldays.</p>
            </div>
        </div>
    """)

print(f"""
        <div class="container">
            <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
                <span class="text-muted">Selected Topics in Mathematical Optimization - 2024</span>
                <span class="text-muted">Robbe Claeys 🐻 & Jovana Filipovic 🐞 </span>
                <a class="text-muted" href="https://github.com/robsyc/InterWay/tree/main"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-github" viewBox="0 0 16 16">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>
                </a>
            </footer>
        </div>
    </body>
</html>
""")