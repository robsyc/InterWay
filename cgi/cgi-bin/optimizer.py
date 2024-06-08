import networkx as nx
import numpy as np
import random

def find_single_path(G, source, target, travel_days, travel_day_max_time):
    """
    Finds a path from source to target that is feasible within the time travel_days * travel_day_max_time
    Returns the path if found, otherwise False
    """
    simple_paths = nx.simple_paths.shortest_simple_paths(G, source=source, target=target, weight="time")

    for simple_path in simple_paths:
        if len(simple_path) >= travel_days + 1:
            # check if the path is feasible within the time travel_days * travel_day_max_time   
            total_time = sum(min(G.edges[simple_path[i], simple_path[i+1]]["time"], travel_day_max_time) for i in range(len(simple_path)-1)) 
            if total_time <= travel_day_max_time * travel_days:
                # make sure that simple_path has length of travel_days
                # indices = np.linspace(0,len(simple_path)-1, travel_days+1, dtype=int)
                initial_path = [simple_path[0]] 
                middle_ind = sorted(random.sample(range(1, len(simple_path)-1), travel_days-1))
                initial_path.extend(simple_path[i] for i in middle_ind)
                initial_path.append(simple_path[-1])
                return initial_path
            else:
                return False
    return False


def get_neighbors_path(G, path):
    """
    Returns a list of paths that are neighbors of the input path
    """
    index = np.random.randint(1,len(path)-1) 
    new_city = G.neighbors(path[index])
    
    neighbor_paths = []
    for city in new_city:
        if city in path:
            continue
        neighbor = path[:index] + [city] + path[index +1:]
        neighbor_paths.append(neighbor)
    
    return neighbor_paths


def shortest_path(G, source, target, weight="time"):
    """
    Returns the shortest path from source to target in the graph G
    """
    path = nx.shortest_path(G, source=source, target=target, weight=weight)
    time_sum = sum([G.edges[path[i], path[i+1]]["time"] for i in range(len(path)-1)])
    return path, time_sum


def check_proposed_path(G, proposed_path, travel_day_max_time):
    """
    Check if a proposed path is valid
    """
    for i, j in zip(proposed_path[:-1], proposed_path[1:]):
        #check if i and j are neighbors or if shortest path is less than travel_day_max_time
        _, time = shortest_path(G, i, j)
        if j in G.neighbors(i) or time < travel_day_max_time:
            continue
        else:
             return False
    return True


def get_path_score(G, path, travel_day_max_time):
    """
    Returns the score of a path (0 if the path is invalid)
    """
    if check_proposed_path(G, path, travel_day_max_time):
        return sum([G.nodes[city]["score"] for city in path[1:-1]])
    else: 
        return 0
    

def get_full_path(G, optimal_path, end):
    """
    Returns the full path with all the intermediate cities
    """
    full_path = []
    for i, j in zip(optimal_path[:-1], optimal_path[1:]):
        path, time = shortest_path(G, i, j)
        full_path += path[:-1]
    full_path.append(end)
    return full_path


def simulated_annealing(G, f, x0, hyperparameters, travel_day_max_time):
    """
    Simple simulated annealing for a one-dimensional continous problem
    Inputs:
        - f : function to be optimized
        - x0 : starting point (float)
        - hyperparameters: dict with
                * Tmax : maximum (starting) temperature
                * Tmin : minimum (stopping) temperature
                * sigma : standard deviation for sampling a neighbor
                * r : rate of cooling
                * NT : number of iterations with fixed temperature --> how many neighbours you choose
    Outputs:
            - xstar : obtained minimum
            - xpath : path of x-values explored
            - fbest : best function values in each iteration
            - temperatures : the temperature of each iteration
    """
    # get hyperparameters
    Tmax = hyperparameters['Tmax']
    Tmin = hyperparameters['Tmin']
    r = hyperparameters['r']
    NT = hyperparameters['NT']

    # init outputs
    x = x0.copy() #current x
    temp = Tmax
    xstar = x.copy() #maximum x
    fstar = f(G, xstar, travel_day_max_time) #maximum score
    xpaths = [x.copy()]
    fpaths = [fstar]
    temperatures = [temp]

    while temp > Tmin:
        for i in range(NT):
            neighbor_paths = get_neighbors_path(G, xstar)
            for neighbor in neighbor_paths:
                fnew = f(G, neighbor, travel_day_max_time)
                if fnew > fstar and fnew > 0:
                    xstar= neighbor.copy()
                    fstar = fnew
                elif  np.exp((-fstar+fnew)/temp*5) > np.random.rand():
                    xstar= neighbor.copy()
                    fstar= fnew

                xpaths.append(xstar.copy())
                fpaths.append(fstar)                            
                temperatures.append(temp)
                temp *= r

    return xstar, xpaths, fpaths, temperatures


def get_paths(G, start, end, total_travel_days, travel_days, travel_day_max_time=9*60):
    """
    Get the best paths from start to end with the given hyperparameters
    Runs simulated annealing algorithm 25 times and returns the best paths
    """
    hyperparameters = {
        'Tmax': 10,
        'Tmin': 0.1,
        'r': 0.95,
        'NT': 20
    }
    path_set = set()
    result = {
        # 'path': [],
        # 'full_path': [],
        # 'score': 0,
        # 'stop_days': []
    }

    for i in range(25):
        path = find_single_path(G, start, end, travel_days, travel_day_max_time)
        if path:
            xstar, xpaths, fpaths, temperatures = simulated_annealing(G, get_path_score, path, hyperparameters, travel_day_max_time)
            path_set.add(tuple(xstar))
        else:
            return False
    
    for i, path in enumerate(path_set):
        if check_proposed_path(G, path, travel_day_max_time):
            score = get_path_score(G, path, travel_day_max_time)
            full_path = get_full_path(G, path, end)
            score_list = [G.nodes[city]["score"] for city in path[1:-1]]
            stop_days = [round((item / score) * total_travel_days) for item in score_list]

            if sum(stop_days) > total_travel_days:
                stop_days[-1] -= 1
            elif sum(stop_days) < total_travel_days:
                stop_days[-1] += 1

            result[i] = {
                'path': path,
                'full_path': full_path,
                'score': score,
                'stop_days': stop_days
            }
    
    return result