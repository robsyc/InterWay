# InterWay

Course project for "Selected Topics in Mathematical Optimization" (STMO) from [Jovana](https://github.com/jovanafilipovic1) and [Robbe](https://github.com/robsyc) <3

We are planning an [Interrail](https://www.interrail.eu/en) vacation starting in Brussels and ending in Belgrade. To plan our vacaction in the most mathimatically sound way, we've translated it into a graph problem...

## Data and tools

- Minimal [Interrail map](https://www.interrail.eu/en/plan-your-trip/interrail-railway-map) of European train routes and their travel time
- [Nominatim geocoder API](https://nominatim.org/) used with [GeoPy](https://geopy.readthedocs.io/en/stable/)
- [NetworkX Python package](https://networkx.org/documentation/stable/index.html) for constructing connected graphs

## Problem

The goal of this project is to find a path through a connected graph - with several constaints:
1. We need to arrive at a specific destination within a certain amount of days
2. Travel days are limited (based on specific [Interrail pass](https://www.interrail.eu/en/interrail-passes/global-pass))
3. Visiting preference of one city over another (based on user input)

Potential additional constrains:
- Aversion towards [reservation-required trips](https://www.interrail.eu/en/book-reservations/reservation-fees) (based on surcharge)

---

# What's in the repo?

- `notebook.ipynb` contains all our code we used during development and can be run from start to finish
- `requirements.txt` contains all necessary packages
- `./data` contains all resources and intermediary files (may need to be unzipped first)

## How to get started `Python 3.11.5`

1. [Activate venv](https://docs.python.org/3/library/venv.html)
- Windows: `.\env\Scripts\activate.bat`
- Mac/Linux: `source ./env/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Open folder in IDE: `code ./` and select `env` kernel

## Running the CGI app

Within `./cgi`

`python -m http.server --cgi` (Run in command line)

Open http://localhost:8000/ 
