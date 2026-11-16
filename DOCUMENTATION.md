# PathFinder GIS Engine: Comprehensive Master Documentation 🇧🇩

A full-stack Geographic Information System (GIS) and heuristic graph routing application built with **Django 6**, **Google Maps JavaScript API**, and **Python Graph Algorithms (BFS, DFS, Dijkstra, A\*)** tailored with real **Bangladesh Jelas & Districts** across all 8 divisions.

---

## Deliverables & Documentation Index

- **Official PDF Documentation:** [`PathFinder_GIS_Bangladesh_Documentation.pdf`](./PathFinder_GIS_Bangladesh_Documentation.pdf) *(2.60 MB)*
- **Annotated Screenshots Directory:** [`screenshots/`](./screenshots/)
  - `marked_01_dashboard.png`: Main dashboard with callouts [1] to [5].
  - `marked_02_a_star_route.png`: A* route with callouts [1] to [3].
  - `marked_03_four_way_comparison.png`: 4-way comparison matrix with callouts [1] to [3].
  - `marked_04_projector_view.png`: High-contrast projector view with callouts [1] to [2].
  - `marked_05_dfs_detour.png`: DFS deep detour route with callouts [1] to [2].
  - `marked_06_django_admin.png`: Django Admin backend with callout [1].

---

## Benchmark Results (Dhaka ➔ Chattogram)

| Algorithm | Shortest Distance | Segment Hops | Nodes Explored | Latency (ms) | Optimality Verdict |
|---|:---:|:---:|:---:|:---:|---|
| **A\* Search** | **232.2 km** | 4 hops | **7 nodes** | **0.34 ms** | **Global Optimum (Fastest & 75.8% Pruned)** |
| **Dijkstra** | **232.2 km** | 4 hops | 29 nodes | 0.58 ms | **Global Optimum (Exhaustive Search)** |
| **BFS** | **232.2 km** | **4 hops** | 30 nodes | 0.22 ms | **Minimum Segment Hops** |
| **DFS** | 1,329.6 km | 20 hops | 26 nodes | 0.19 ms | **Suboptimal Detour (+1,097 km excess)** |

---

## Setup & Quick Start

```powershell
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_graph
python manage.py test routing
python manage.py runserver 127.0.0.1:8000
```
Open **http://127.0.0.1:8000/** in your browser.
Django Admin: **http://127.0.0.1:8000/admin/** (`admin` / `admin123`).
