from django.test import TestCase, Client
from routing.models import Node, Edge
from routing.algorithms import (
    load_graph_from_db,
    bfs_algorithm,
    dfs_algorithm,
    dijkstra_algorithm,
    a_star_algorithm,
    execute_pathfinding,
    execute_all_comparison
)

class PathfinderTests(TestCase):
    def setUp(self):
        # Create a small network: Point A -> Point B -> Point C
        self.node_a = Node.objects.create(code="TEST_A", name="Point A", bn_name="পয়েন্ট এ", division="Test", region="test", latitude=23.70, longitude=90.30)
        self.node_b = Node.objects.create(code="TEST_B", name="Point B", bn_name="পয়েন্ট বি", division="Test", region="test", latitude=23.71, longitude=90.30)
        self.node_c = Node.objects.create(code="TEST_C", name="Point C", bn_name="পয়েন্ট সি", division="Test", region="test", latitude=23.72, longitude=90.30)

        # A-B is 1.2 km, B-C is 1.2 km (total 2.4 km)
        # Detour edge A-C is 15.0 km
        self.edge_ab = Edge.objects.create(source=self.node_a, destination=self.node_b, distance_km=1.2, is_bidirectional=True)
        self.edge_bc = Edge.objects.create(source=self.node_b, destination=self.node_c, distance_km=1.2, is_bidirectional=True)
        self.edge_ac = Edge.objects.create(source=self.node_a, destination=self.node_c, distance_km=15.0, is_bidirectional=True)

    def test_dijkstra_finds_optimal_path(self):
        nodes_dict, adjacency = load_graph_from_db(region="test")
        result = dijkstra_algorithm("TEST_A", "TEST_C", nodes_dict, adjacency)
        self.assertTrue(result["success"])
        self.assertEqual(result["path"], ["TEST_A", "TEST_B", "TEST_C"])
        self.assertEqual(result["total_distance_km"], 2.4)

    def test_a_star_finds_optimal_path(self):
        nodes_dict, adjacency = load_graph_from_db(region="test")
        result = a_star_algorithm("TEST_A", "TEST_C", nodes_dict, adjacency)
        self.assertTrue(result["success"])
        self.assertEqual(result["path"], ["TEST_A", "TEST_B", "TEST_C"])
        self.assertEqual(result["total_distance_km"], 2.4)

    def test_bfs_algorithm(self):
        nodes_dict, adjacency = load_graph_from_db(region="test")
        result = bfs_algorithm("TEST_A", "TEST_C", nodes_dict, adjacency)
        self.assertTrue(result["success"])
        # BFS looks for minimum hops; direct edge A-C has 1 hop
        self.assertEqual(result["hops"], 1)
        self.assertEqual(result["path"], ["TEST_A", "TEST_C"])

    def test_dfs_algorithm(self):
        nodes_dict, adjacency = load_graph_from_db(region="test")
        result = dfs_algorithm("TEST_A", "TEST_C", nodes_dict, adjacency)
        self.assertTrue(result["success"])
        self.assertIn("TEST_A", result["path"])
        self.assertIn("TEST_C", result["path"])

    def test_4_way_comparison_api(self):
        client = Client()
        resp = client.get('/api/compare/?source=TEST_A&destination=TEST_C&region=test')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        algorithms = data["comparison"]["algorithms"]
        self.assertIn("bfs", algorithms)
        self.assertIn("dfs", algorithms)
        self.assertIn("dijkstra", algorithms)
        self.assertIn("a_star", algorithms)
