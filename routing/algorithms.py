import heapq
import time
import math
from collections import deque
from .models import Node, Edge

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Great-circle distance between two points on Earth in kilometers.
    """
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)

def load_graph_from_db(region=None):
    """
    Constructs an in-memory graph representation from Django database models.
    Can be filtered by geographic network ('bangladesh' or 'dhaka').
    """
    nodes_qs = Node.objects.all()
    if region:
        nodes_qs = nodes_qs.filter(region=region)

    edges_qs = Edge.objects.select_related('source', 'destination').all()
    if region:
        edges_qs = edges_qs.filter(source__region=region, destination__region=region)

    nodes_dict = {
        n.code: {
            "id": n.id,
            "code": n.code,
            "name": n.name,
            "bn_name": n.bn_name,
            "division": n.division,
            "region": n.region,
            "lat": n.latitude,
            "lng": n.longitude,
            "description": n.description,
        }
        for n in nodes_qs
    }

    adjacency = {code: {} for code in nodes_dict}

    for edge in edges_qs:
        src = edge.source.code
        dst = edge.destination.code
        dist = edge.distance_km if edge.distance_km is not None else edge.source.distance_to(edge.destination)

        if src in adjacency and dst in adjacency:
            adjacency[src][dst] = dist
            if edge.is_bidirectional:
                adjacency[dst][src] = dist

    return nodes_dict, adjacency

def a_star_heuristic(node_code, goal_code, nodes_dict):
    """
    Admissible and consistent straight-line distance heuristic for A*.
    h(n) <= true shortest distance, ensuring optimal path finding.
    """
    n1 = nodes_dict[node_code]
    n2 = nodes_dict[goal_code]
    return haversine_distance(n1["lat"], n1["lng"], n2["lat"], n2["lng"])

def calculate_path_distance(path, adjacency):
    """
    Computes total highway distance in kilometers for a given path sequence.
    """
    total = 0.0
    for i in range(len(path) - 1):
        total += adjacency.get(path[i], {}).get(path[i + 1], 0.0)
    return round(total, 3)

# -------------------------------------------------------------
# 1. BFS (Breadth-First Search) Algorithm
# -------------------------------------------------------------
def bfs_algorithm(start_code, goal_code, nodes_dict, adjacency):
    """
    Breadth-First Search (BFS).
    Unweighted shortest path algorithm. Guarantees minimum number of edges (hops),
    but does NOT consider edge road distances.
    """
    start_time = time.perf_counter()

    queue = deque([start_code])
    visited = {start_code}
    previous = {start_code: None}
    explored_nodes_log = []

    found = False
    while queue:
        curr_node = queue.popleft()
        explored_nodes_log.append(curr_node)

        if curr_node == goal_code:
            found = True
            break

        # Explore neighbors
        for neighbor in sorted(adjacency.get(curr_node, {}).keys()):
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = curr_node
                queue.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if not found:
        return {
            "success": False,
            "algorithm": "BFS",
            "message": f"No navigable path exists between {start_code} and {goal_code}"
        }

    # Reconstruct path
    path = []
    curr = goal_code
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    total_dist = calculate_path_distance(path, adjacency)

    return {
        "success": True,
        "algorithm": "BFS (Breadth-First Search)",
        "short_name": "BFS",
        "path": path,
        "hops": len(path) - 1,
        "total_distance_km": total_dist,
        "execution_time_ms": round(elapsed_ms, 4),
        "nodes_explored": len(explored_nodes_log),
        "explored_sequence": explored_nodes_log,
        "characteristics": "Minimum segment hops; unweighted traversal."
    }

# -------------------------------------------------------------
# 2. DFS (Depth-First Search) Algorithm
# -------------------------------------------------------------
def dfs_algorithm(start_code, goal_code, nodes_dict, adjacency):
    """
    Depth-First Search (DFS).
    Explores as deep as possible along each branch before backtracking.
    Finds a valid path, but often takes long detours and is NOT optimal for routing.
    """
    start_time = time.perf_counter()

    stack = [start_code]
    visited = set()
    previous = {start_code: None}
    explored_nodes_log = []
    found = False

    while stack:
        curr_node = stack.pop()

        if curr_node in visited:
            continue
        visited.add(curr_node)
        explored_nodes_log.append(curr_node)

        if curr_node == goal_code:
            found = True
            break

        # Push unvisited neighbors onto stack
        for neighbor in sorted(adjacency.get(curr_node, {}).keys(), reverse=True):
            if neighbor not in visited:
                previous[neighbor] = curr_node
                stack.append(neighbor)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    if not found:
        return {
            "success": False,
            "algorithm": "DFS",
            "message": f"No navigable path exists between {start_code} and {goal_code}"
        }

    # Reconstruct path
    path = []
    curr = goal_code
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    total_dist = calculate_path_distance(path, adjacency)

    return {
        "success": True,
        "algorithm": "DFS (Depth-First Search)",
        "short_name": "DFS",
        "path": path,
        "hops": len(path) - 1,
        "total_distance_km": total_dist,
        "execution_time_ms": round(elapsed_ms, 4),
        "nodes_explored": len(explored_nodes_log),
        "explored_sequence": explored_nodes_log,
        "characteristics": "Deep branch exploration; creates detours; non-optimal distance."
    }

# -------------------------------------------------------------
# 3. Dijkstra's Algorithm
# -------------------------------------------------------------
def dijkstra_algorithm(start_code, goal_code, nodes_dict, adjacency):
    """
    Dijkstra's Shortest Path Algorithm.
    Uniform-cost search exploring outward by lowest cumulative distance.
    Guarantees global minimum distance on non-negative weighted graphs.
    """
    start_time = time.perf_counter()

    pq = [(0.0, start_code)]
    distances = {node: float("inf") for node in adjacency}
    distances[start_code] = 0.0
    previous = {node: None for node in adjacency}
    visited = set()
    explored_nodes_log = []

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_node in visited:
            continue
        visited.add(curr_node)
        explored_nodes_log.append(curr_node)

        if curr_node == goal_code:
            break

        for neighbor, weight in adjacency.get(curr_node, {}).items():
            tentative = curr_dist + weight
            if tentative < distances[neighbor]:
                distances[neighbor] = tentative
                previous[neighbor] = curr_node
                heapq.heappush(pq, (tentative, neighbor))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    path = []
    curr = goal_code
    while curr is not None:
        path.append(curr)
        curr = previous[curr]
    path.reverse()

    if not path or path[0] != start_code:
        return {
            "success": False,
            "algorithm": "Dijkstra",
            "message": f"No navigable path exists between {start_code} and {goal_code}"
        }

    return {
        "success": True,
        "algorithm": "Dijkstra’s Algorithm",
        "short_name": "Dijkstra",
        "path": path,
        "hops": len(path) - 1,
        "total_distance_km": round(distances[goal_code], 3),
        "execution_time_ms": round(elapsed_ms, 4),
        "nodes_explored": len(explored_nodes_log),
        "explored_sequence": explored_nodes_log,
        "characteristics": "Guaranteed minimum road distance; uniform radial search."
    }

# -------------------------------------------------------------
# 4. A* (A-Star) Search Algorithm
# -------------------------------------------------------------
def a_star_algorithm(start_code, goal_code, nodes_dict, adjacency):
    """
    A* (A-Star) Pathfinding Algorithm.
    Informed search using f(n) = g(n) + h(n), where h(n) is the Haversine distance heuristic.
    Guarantees minimum distance while minimizing search space expansion.
    """
    start_time = time.perf_counter()

    h_start = a_star_heuristic(start_code, goal_code, nodes_dict)
    open_set = [(h_start, 0.0, start_code)]
    
    g_scores = {node: float("inf") for node in adjacency}
    g_scores[start_code] = 0.0
    came_from = {node: None for node in adjacency}
    visited = set()
    explored_nodes_log = []

    while open_set:
        _, curr_g, curr_node = heapq.heappop(open_set)

        if curr_node in visited:
            continue
        visited.add(curr_node)
        explored_nodes_log.append(curr_node)

        if curr_node == goal_code:
            break

        for neighbor, weight in adjacency.get(curr_node, {}).items():
            tentative_g = curr_g + weight
            if tentative_g < g_scores[neighbor]:
                came_from[neighbor] = curr_node
                g_scores[neighbor] = tentative_g
                f_score = tentative_g + a_star_heuristic(neighbor, goal_code, nodes_dict)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    path = []
    curr = goal_code
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()

    if not path or path[0] != start_code:
        return {
            "success": False,
            "algorithm": "A*",
            "message": f"No navigable path exists between {start_code} and {goal_code}"
        }

    return {
        "success": True,
        "algorithm": "A* (A-Star) Search",
        "short_name": "A*",
        "path": path,
        "hops": len(path) - 1,
        "total_distance_km": round(g_scores[goal_code], 3),
        "execution_time_ms": round(elapsed_ms, 4),
        "nodes_explored": len(explored_nodes_log),
        "explored_sequence": explored_nodes_log,
        "characteristics": "Goal-directed heuristic search; optimal distance with minimal expansion."
    }

def build_itinerary(path, nodes_dict, adjacency):
    """
    Builds turn-by-turn itinerary segments with individual and cumulative distances.
    """
    itinerary = []
    cumulative = 0.0
    for i in range(len(path)):
        node_code = path[i]
        node = nodes_dict[node_code]
        seg_dist = 0.0
        if i > 0:
            prev_code = path[i - 1]
            seg_dist = adjacency.get(prev_code, {}).get(node_code, 0.0)
            cumulative += seg_dist

        itinerary.append({
            "step": i + 1,
            "code": node_code,
            "name": node["name"],
            "bn_name": node.get("bn_name", ""),
            "division": node.get("division", ""),
            "lat": node["lat"],
            "lng": node["lng"],
            "segment_distance_km": round(seg_dist, 3),
            "cumulative_distance_km": round(cumulative, 3),
        })
    return itinerary

def execute_pathfinding(algorithm_choice, start_code, goal_code, region=None):
    """
    Main executor supporting BFS, DFS, Dijkstra, and A*.
    """
    if not region:
        sample_node = Node.objects.filter(code=start_code).first()
        if sample_node:
            region = sample_node.region

    nodes_dict, adjacency = load_graph_from_db(region=region)

    if start_code not in nodes_dict or goal_code not in nodes_dict:
        return {
            "success": False,
            "message": f"Invalid start ({start_code}) or goal ({goal_code}) node."
        }

    if start_code == goal_code:
        node = nodes_dict[start_code]
        return {
            "success": True,
            "algorithm": algorithm_choice,
            "path": [start_code],
            "total_distance_km": 0.0,
            "execution_time_ms": 0.01,
            "nodes_explored": 1,
            "explored_sequence": [start_code],
            "itinerary": [{
                "step": 1,
                "code": start_code,
                "name": node["name"],
                "bn_name": node.get("bn_name", ""),
                "division": node.get("division", ""),
                "lat": node["lat"],
                "lng": node["lng"],
                "segment_distance_km": 0.0,
                "cumulative_distance_km": 0.0,
            }],
            "route_coordinates": [{"lat": node["lat"], "lng": node["lng"]}],
        }

    choice = algorithm_choice.lower().strip()
    if choice in ["bfs", "breadth_first"]:
        result = bfs_algorithm(start_code, goal_code, nodes_dict, adjacency)
    elif choice in ["dfs", "depth_first"]:
        result = dfs_algorithm(start_code, goal_code, nodes_dict, adjacency)
    elif choice in ["a_star", "astar", "a*"]:
        result = a_star_algorithm(start_code, goal_code, nodes_dict, adjacency)
    else:
        result = dijkstra_algorithm(start_code, goal_code, nodes_dict, adjacency)

    if result["success"]:
        result["itinerary"] = build_itinerary(result["path"], nodes_dict, adjacency)
        result["route_coordinates"] = [
            {"lat": nodes_dict[code]["lat"], "lng": nodes_dict[code]["lng"]}
            for code in result["path"]
        ]

    return result

def execute_all_comparison(start_code, goal_code, region=None):
    """
    Runs all 4 algorithms (BFS, DFS, Dijkstra, A*) and returns complete comparative benchmark.
    """
    if not region:
        sample_node = Node.objects.filter(code=start_code).first()
        if sample_node:
            region = sample_node.region

    nodes_dict, adjacency = load_graph_from_db(region=region)

    if start_code not in nodes_dict or goal_code not in nodes_dict:
        return {
            "success": False,
            "message": f"Invalid start ({start_code}) or goal ({goal_code}) node."
        }

    bfs_res = bfs_algorithm(start_code, goal_code, nodes_dict, adjacency)
    dfs_res = dfs_algorithm(start_code, goal_code, nodes_dict, adjacency)
    dijkstra_res = dijkstra_algorithm(start_code, goal_code, nodes_dict, adjacency)
    a_star_res = a_star_algorithm(start_code, goal_code, nodes_dict, adjacency)

    for res in [bfs_res, dfs_res, dijkstra_res, a_star_res]:
        if res["success"]:
            res["itinerary"] = build_itinerary(res["path"], nodes_dict, adjacency)
            res["route_coordinates"] = [
                {"lat": nodes_dict[c]["lat"], "lng": nodes_dict[c]["lng"]} for c in res["path"]
            ]

    total_nodes = len(nodes_dict)
    min_dist = dijkstra_res.get("total_distance_km", 0.0)

    return {
        "success": True,
        "region": region,
        "total_network_nodes": total_nodes,
        "start": {
            "code": start_code,
            "name": nodes_dict[start_code]["name"],
            "bn_name": nodes_dict[start_code].get("bn_name", ""),
            "division": nodes_dict[start_code].get("division", ""),
            "lat": nodes_dict[start_code]["lat"],
            "lng": nodes_dict[start_code]["lng"]
        },
        "goal": {
            "code": goal_code,
            "name": nodes_dict[goal_code]["name"],
            "bn_name": nodes_dict[goal_code].get("bn_name", ""),
            "division": nodes_dict[goal_code].get("division", ""),
            "lat": nodes_dict[goal_code]["lat"],
            "lng": nodes_dict[goal_code]["lng"]
        },
        "algorithms": {
            "bfs": bfs_res,
            "dfs": dfs_res,
            "dijkstra": dijkstra_res,
            "a_star": a_star_res,
        },
        "summary": {
            "optimal_distance_km": min_dist,
            "astar_nodes_saved": dijkstra_res.get("nodes_explored", 0) - a_star_res.get("nodes_explored", 0),
            "dfs_excess_distance_km": round(max(0, dfs_res.get("total_distance_km", 0) - min_dist), 3),
            "bfs_hops": bfs_res.get("hops", 0),
            "dijkstra_hops": dijkstra_res.get("hops", 0),
        }
    }
