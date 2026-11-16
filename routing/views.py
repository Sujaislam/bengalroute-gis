import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Node, Edge
from .algorithms import execute_pathfinding, execute_all_comparison, load_graph_from_db

def index(request):
    """
    Renders main interactive map interface.
    Passes nodes, divisions, edges, regions, and Google Maps API key to the template.
    """
    divisions = list(Node.objects.filter(region="bangladesh").values_list('division', flat=True).distinct().order_by('division'))
    bd_nodes = Node.objects.filter(region="bangladesh").order_by('division', 'name')
    dhk_nodes = Node.objects.filter(region="dhaka").order_by('name')

    context = {
        "divisions": divisions,
        "bd_nodes": bd_nodes,
        "dhk_nodes": dhk_nodes,
        "google_maps_api_key": getattr(settings, "GOOGLE_MAPS_API_KEY", ""),
    }
    return render(request, "index.html", context)

def api_graph(request):
    """
    Returns full graph network (nodes & edges) filtered by region.
    Query param: ?region=bangladesh (default) or ?region=dhaka
    """
    region = request.GET.get("region", "bangladesh").lower()
    nodes_dict, adjacency = load_graph_from_db(region=region)
    
    edges_qs = Edge.objects.select_related('source', 'destination')
    if region:
        edges_qs = edges_qs.filter(source__region=region, destination__region=region)

    edges_data = [
        {
            "source": e.source.code,
            "destination": e.destination.code,
            "distance_km": e.distance_km,
            "is_bidirectional": e.is_bidirectional,
        }
        for e in edges_qs
    ]

    divisions = sorted(list({n.get("division") for n in nodes_dict.values() if n.get("division")}))

    return JsonResponse({
        "status": "success",
        "region": region,
        "divisions": divisions,
        "nodes": nodes_dict,
        "edges": edges_data,
        "total_nodes": len(nodes_dict),
        "total_edges": len(edges_data),
    })

@csrf_exempt
def find_path(request):
    """
    API endpoint to execute pathfinding algorithm.
    Accepts GET query parameters or POST JSON payload:
      - source (e.g. 'BD_DHK')
      - destination (e.g. 'BD_CTG')
      - algorithm ('bfs', 'dfs', 'dijkstra', or 'a_star')
      - region ('bangladesh' or 'dhaka')
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            data = request.POST
        source = data.get("source")
        destination = data.get("destination")
        algorithm = data.get("algorithm", "dijkstra")
        region = data.get("region")
    else:
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        algorithm = request.GET.get("algorithm", "dijkstra")
        region = request.GET.get("region")

    if not source or not destination:
        return JsonResponse({
            "status": "error",
            "message": "Both source and destination must be provided."
        }, status=400)

    result = execute_pathfinding(algorithm, source.strip(), destination.strip(), region=region)
    
    if not result.get("success"):
        return JsonResponse({"status": "error", "message": result.get("message")}, status=404)

    return JsonResponse({"status": "success", "result": result})

@csrf_exempt
def compare_algorithms(request):
    """
    API endpoint comparing BFS, DFS, Dijkstra, and A* performance metrics side-by-side.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, AttributeError):
            data = request.POST
        source = data.get("source")
        destination = data.get("destination")
        region = data.get("region")
    else:
        source = request.GET.get("source")
        destination = request.GET.get("destination")
        region = request.GET.get("region")

    if not source or not destination:
        return JsonResponse({
            "status": "error",
            "message": "Both source and destination must be provided."
        }, status=400)

    comparison = execute_all_comparison(source.strip(), destination.strip(), region=region)

    if not comparison.get("success"):
        return JsonResponse({"status": "error", "message": comparison.get("message")}, status=404)

    return JsonResponse({"status": "success", "comparison": comparison})
