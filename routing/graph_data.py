import math

# 15 Manually defined landmark nodes in Manhattan
NODES = {
    "N1":  {"id": "N1",  "name": "Times Square",              "lat": 40.7580, "lng": -73.9855},
    "N2":  {"id": "N2",  "name": "Bryant Park",               "lat": 40.7536, "lng": -73.9832},
    "N3":  {"id": "N3",  "name": "Grand Central Terminal",    "lat": 40.7527, "lng": -73.9772},
    "N4":  {"id": "N4",  "name": "Rockefeller Center",         "lat": 40.7587, "lng": -73.9787},
    "N5":  {"id": "N5",  "name": "MoMA (Museum of Modern Art)","lat": 40.7614, "lng": -73.9776},
    "N6":  {"id": "N6",  "name": "Columbus Circle",           "lat": 40.7681, "lng": -73.9819},
    "N7":  {"id": "N7",  "name": "Central Park South",        "lat": 40.7656, "lng": -73.9760},
    "N8":  {"id": "N8",  "name": "Empire State Building",     "lat": 40.7484, "lng": -73.9857},
    "N9":  {"id": "N9",  "name": "Madison Square Park",       "lat": 40.7420, "lng": -73.9880},
    "N10": {"id": "N10", "name": "Flatiron Building",         "lat": 40.7411, "lng": -73.9897},
    "N11": {"id": "N11", "name": "Union Square",              "lat": 40.7359, "lng": -73.9911},
    "N12": {"id": "N12", "name": "Washington Square Park",    "lat": 40.7308, "lng": -73.9973},
    "N13": {"id": "N13", "name": "High Line (North Entrance)", "lat": 40.7540, "lng": -74.0020},
    "N14": {"id": "N14", "name": "Chelsea Market",            "lat": 40.7424, "lng": -74.0061},
    "N15": {"id": "N15", "name": "Hudson Yards",              "lat": 40.7539, "lng": -74.0006},
}

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    R = 6371.0  # Earth's radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2.0) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 3)

# Raw undirected edges connecting nodes
RAW_EDGES = [
    ("N1", "N2"),
    ("N1", "N4"),
    ("N1", "N6"),
    ("N1", "N13"),
    ("N2", "N3"),
    ("N2", "N8"),
    ("N3", "N4"),
    ("N4", "N5"),
    ("N5", "N7"),
    ("N6", "N7"),
    ("N6", "N15"),
    ("N8", "N9"),
    ("N8", "N15"),
    ("N9", "N10"),
    ("N9", "N14"),
    ("N10", "N11"),
    ("N11", "N12"),
    ("N12", "N14"),
    ("N13", "N15"),
    ("N14", "N15"),
]

def build_graph():
    """
    Builds an adjacency list representation of the graph.
    Returns:
        dict: { node_id: { neighbor_id: distance_km, ... } }
    """
    graph = {node_id: {} for node_id in NODES}
    for u, v in RAW_EDGES:
        dist = haversine_distance(
            NODES[u]["lat"], NODES[u]["lng"],
            NODES[v]["lat"], NODES[v]["lng"]
        )
        graph[u][v] = dist
        graph[v][u] = dist
    return graph

GRAPH = build_graph()
