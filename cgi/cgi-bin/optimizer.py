import networkx as nx
import random

# shortest path 
def shortest_path(G, source, target, weight="time"):
    path = nx.shortest_path(G, source=source, target=target, weight=weight)
    time_sum = sum([G.edges[path[i], path[i+1]]["time"] for i in range(len(path)-1)])
    return path, time_sum

## find possible paths
def shuffle_path(path):
    temp = path.copy()
    random.shuffle(temp)
    return temp

def get_n_highest_scoring_cities(G, path, n):
    shuffled_path = shuffle_path(path[1:-1])
    city_scores = {city: G.nodes[city]["score"] for city in shuffled_path}
    max_scores = sorted(city_scores, key=city_scores.get, reverse=True)[:n]
    return max_scores

def check_proposed_path(G, proposed_path, travel_day_max_time, travel_days=4):
    path = proposed_path.copy()
    max_scores = get_n_highest_scoring_cities(G, path, n=travel_days)
    # propsed path, only including the highest scoring cities
    for city in proposed_path[1:-1]:
        if city not in max_scores:
            path.remove(city)
    # travel time between cities of proposed path
    for i, j in zip(path[:-1], path[1:]):
        _, time = shortest_path(G, i, j)
        if time > travel_day_max_time:
            return False
    return tuple(path)

def get_path_score(G, path):
    return sum([G.nodes[city]["score"] for city in path[1:-1]])

def get_first_n_simple_paths(G, source, target, travel_days=4, n_iter=100, travel_day_max_time=9*60):
    simple_paths = nx.shortest_simple_paths(G, source, target, weight="time")
    possible_paths = set()
    i = 0
    for proposed_path in simple_paths:
        i += 1
        path = check_proposed_path(G, proposed_path, travel_day_max_time, travel_days=travel_days)
        if path:
            score = get_path_score(G, path)
            possible_paths.add((path, score))
        if i == n_iter:
            break
    return possible_paths

def get_full_path(G, optimal_path, end):
    full_path = []
    for i, j in zip(optimal_path[:-1], optimal_path[1:]):
        path, time = shortest_path(G, i, j)
        full_path += path[:-1]
    full_path.append(end)
    return full_path

def get_paths(G, start, end, total_travel_days, travel_days, travel_day_max_time=9*60):
    paths = []
    stop_days_list = []
    full_paths = []

    possible_paths = get_first_n_simple_paths(G, start, end, travel_days=travel_days, n_iter=1000, travel_day_max_time=travel_day_max_time)
    sorted_paths = sorted(possible_paths, key=lambda x: x[1], reverse=True)

    for i in range(5):
        path, tot_score = sorted_paths[i]
        score_list = [G.nodes[city]["score"] for city in path[1:-1]]
        stop_days = [round((item / tot_score) * total_travel_days) for item in score_list]

        if sum(stop_days) > total_travel_days:
            stop_days[-1] -= 1
        elif sum(stop_days) < total_travel_days:
            stop_days[-1] += 1

        full_path = get_full_path(G, path, end)

        paths.append(path)
        stop_days_list.append(stop_days)
        full_paths.append(full_path)
        
    return paths, stop_days_list, full_paths