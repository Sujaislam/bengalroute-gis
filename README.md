# BengalRoute GIS Engine: Bangladesh Jela & District Edition 🇧🇩

A full-stack Geographic Information System (GIS) and heuristic graph routing application built with **Django**, **Google Maps JavaScript API**, and **Python Graph Algorithms (BFS, DFS, Dijkstra, A\*)**.

---

## 📋 Deliverables Summary

- ✅ **Django Project Files:** Complete, production-grade codebase with SQLite database, Django models, admin panel, REST APIs, and responsive UI.
- ✅ **Pathfinding Algorithms (4 Total):**
  1. **BFS (Breadth-First Search):** Unweighted shortest-hop routing.
  2. **DFS (Depth-First Search):** Deep branch traversal demonstrating routing detours.
  3. **Dijkstra’s Algorithm:** Weighted uniform-cost search guaranteeing absolute shortest road distance.
  4. **A\* (A-Star) Search:** Informed heuristic search using admissible Haversine straight-line distance.
- ✅ **Part C 4-Way Comparative Benchmark:** Real-time side-by-side performance matrix of BFS vs. DFS vs. Dijkstra vs. A*.
- ✅ **Bangladesh Jelas & Districts Network:** 32 interconnected districts across all 8 divisions with English & Bangla names and Division filters.
- ✅ **Dhaka Metropolitan Network:** 16 landmark micro-transit hubs.
- ✅ **Sample Output Screenshots:** Automated screenshots saved in [`screenshots/`](./screenshots/).

---

## 🗺️ Bangladesh Jelas & Districts Dataset (32 Jelas across 8 Divisions)

| Division (বিভাগ) | Districts / Jelas (জেলা) Included |
|---|---|
| **Dhaka (ঢাকা)** | Dhaka (ঢাকা), Gazipur (গাজীপুর), Narayanganj (নারায়ণগঞ্জ), Tangail (টাঙ্গাইল), Faridpur (ফরিদপুর), Narsingdi (নরসিংদী), Manikganj (মানিকগঞ্জ), Gopalganj (গোপালগঞ্জ) |
| **Chattogram (চট্টগ্রাম)** | Chattogram (চট্টগ্রাম), Cox's Bazar (কক্সবাজার), Cumilla (কুমিল্লা), Feni (ফেনী), Brahmanbaria (ব্রাহ্মণবাড়িয়া), Noakhali (নোয়াখালী), Chandpur (চাঁদপুর) |
| **Sylhet (সিলেট)** | Sylhet (সিলেট), Moulvibazar (মৌলভীবাজার), Habiganj (হবিগঞ্জ) |
| **Rajshahi (রাজশাহী)** | Rajshahi (রাজশাহী), Bogura (বগুড়া), Pabna (পাবনা), Sirajganj (সিরাজগঞ্জ), Natore (নাটোর) |
| **Rangpur (রংপুর)** | Rangpur (রংপুর), Dinajpur (দিনাজপুর), Gaibandha (গাইবান্ধা) |
| **Khulna (খুলনা)** | Khulna (খুলনা), Jashore (যশোর), Kushtia (কুষ্টিয়া) |
| **Barishal (বরিশাল)** | Barishal (বরিশাল), Patuakhali (পটুয়াখালী) |
| **Mymensingh (ময়মনসিংহ)** | Mymensingh (ময়মনসিংহ) |

---

## ⚡ Algorithmic Behavior Comparison (Dhaka ➔ Chattogram)

| Algorithm | Shortest Distance | Segment Hops | Nodes Explored | Execution Time | Optimality Verdict |
|---|---|---|---|---|---|
| **A\* Search** | **232.2 km** | 4 hops | **7 nodes** | **0.34 ms** | **Global Optimum (Fastest & Pruned)** |
| **Dijkstra** | **232.2 km** | 4 hops | **29 nodes** | **0.58 ms** | **Global Optimum (Exhaustive)** |
| **BFS** | **232.2 km** | **4 hops** | 30 nodes | 0.22 ms | **Minimum Hops (Unweighted)** |
| **DFS** | 1329.6 km | 20 hops | 26 nodes | 0.19 ms | **Non-Optimal Detour** |

> [!TIP]
> **Key Pedagogical Takeaway:**
> - **Dijkstra and A\*** both guarantee the exact same global minimum distance (**232.2 km**).
> - **A\*** explored **only 7 nodes** compared to **Dijkstra’s 29 nodes** — eliminating **75.8%** of the search space because its Haversine heuristic directed search straight toward Chattogram.
> - **BFS** found a 4-hop path because it evaluates solely by level depth.
> - **DFS** meandered through 20 hops and 1,329 km, visually demonstrating why DFS is unsuitable for shortest path routing on weighted road graphs.

---

## 📸 Deliverable Annotated Screenshots & PDF Documentation

- **Official Master PDF Documentation:** [`PathFinder_GIS_Bangladesh_Documentation.pdf`](./PathFinder_GIS_Bangladesh_Documentation.pdf) (3.28 MB)

All screenshots are annotated with on-element title tabs, dual-contrast borders, and technical demonstration legends in [`screenshots/`](./screenshots/):
1. **`marked_01_dashboard.png`**: Complete dashboard displaying 32 Bangladesh Jelas, Division filter, presets, and Google Maps live layer.
2. **`marked_02_a_star_route.png`**: Optimal 232.2 km route polyline, performance metric cards (0.34 ms), and step-by-step itinerary.
3. **`marked_03_four_way_comparison.png`**: Part C side-by-side benchmark matrix (BFS vs. DFS vs. Dijkstra vs. A*) and search space expansion bars.
4. **`marked_04_dfs_detour.png`**: Suboptimal DFS traversal demonstrating a 1,329.6 km detour (+1,097.4 km excess penalty) and 20 hops.
5. **`marked_05_projector_view.png`**: High-contrast WCAG 2.1 AA light mode designed for presentation projectors.
6. **`marked_06_dhaka_metro.png`**: High-density 16-node transit network within the Dhaka metropolitan area.
7. **`marked_07_django_admin.png`**: Administrative CRUD backend (`/admin/`) managing `Node` and `Edge` database models.

---

## 🚀 Setup & Execution Guide

### 1. Requirements
- Python 3.10+
- Django 6+ (`pip install -r requirements.txt`)

### 2. Database Migration & Graph Seeding
```powershell
python manage.py makemigrations routing
python manage.py migrate
python manage.py seed_graph
```

### 3. Launch Development Server
```powershell
python manage.py runserver 127.0.0.1:8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

### 4. Run Automated Unit Tests
```powershell
python manage.py test routing
```

### 5. Capture Live Screenshots
```powershell
python capture_screenshots.py
```

### 6. Django Admin Access
- URL: **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)**
- Username: `admin`
- Password: `admin123`
