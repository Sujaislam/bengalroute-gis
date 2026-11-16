import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    try:
        font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def create_annotated_image(input_path, output_path, highlights, legend_title, legend_items):
    base_img = Image.open(input_path).convert("RGBA")
    w, h = base_img.size

    # Legend height dynamically sized based on item count
    rows = (len(legend_items) + 1) // 2
    legend_h = max(190, 55 + rows * 50)
    new_h = h + legend_h
    canvas = Image.new("RGBA", (w, new_h), (15, 23, 42, 255)) # Dark slate-950
    canvas.paste(base_img, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # 1. Draw Highlights & Badges on Screenshot
    font_badge = get_font(18, bold=True)
    
    for item in highlights:
        x1, y1, x2, y2 = item["box"]
        col_hex = item["color"]
        r, g, b = int(col_hex[1:3], 16), int(col_hex[3:5], 16), int(col_hex[5:7], 16)
        
        # Outer white contrast outline
        draw.rounded_rectangle([x1 - 1, y1 - 1, x2 + 1, y2 + 1], radius=6, outline=(255, 255, 255, 180), width=1)
        # Main thick colored border
        draw.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=(r, g, b, 255), width=4)

        # Large Circular Number Badge (34px diameter)
        badge_r = 18
        bx = item.get("badge_x", x1 + 18)
        by = item.get("badge_y", y1 + 18)
        
        draw.ellipse([bx - badge_r - 2, by - badge_r - 2, bx + badge_r + 2, by + badge_r + 2], fill=(255, 255, 255, 255))
        draw.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r], fill=(r, g, b, 255))
        
        n_str = str(item["num"])
        bbox = font_badge.getbbox(n_str)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((bx - nw / 2, by - nh / 2 - 2), n_str, fill=(255, 255, 255), font=font_badge)

    # 2. Draw Legend Divider
    draw.line([(0, h), (w, h)], fill=(51, 65, 85, 255), width=3)
    
    # Legend Header
    font_legend_hdr = get_font(14, bold=True)
    draw.text((25, h + 12), f"📌 WHAT THIS SCREENSHOT DEMONSTRATES: {legend_title.upper()}", fill=(245, 158, 11, 255), font=font_legend_hdr)

    # 3. Draw Legend Items in 2 Columns
    font_title = get_font(14, bold=True)
    font_desc = get_font(13, bold=False)
    
    col1_x = 25
    col2_x = 720
    start_y = h + 42
    row_h = 50

    for idx, leg in enumerate(legend_items):
        col_x = col1_x if idx % 2 == 0 else col2_x
        row_idx = idx // 2
        curr_y = start_y + (row_idx * row_h)

        col_hex = leg["color"]
        r, g, b = int(col_hex[1:3], 16), int(col_hex[3:5], 16), int(col_hex[5:7], 16)

        # Legend Badge
        lb_cx = col_x + 15
        lb_cy = curr_y + 12
        draw.ellipse([lb_cx - 14, lb_cy - 14, lb_cx + 14, lb_cy + 14], fill=(r, g, b, 255), outline=(255, 255, 255, 255), width=2)
        
        n_str = str(leg["num"])
        bbox = font_badge.getbbox(n_str)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((lb_cx - nw / 2, lb_cy - nh / 2 - 2), n_str, fill=(255, 255, 255), font=font_badge)

        # Title & Description
        draw.text((col_x + 38, curr_y), leg["title"], fill=(255, 255, 255), font=font_title)
        draw.text((col_x + 38, curr_y + 20), leg["desc"], fill=(203, 213, 225), font=font_desc)

    canvas.convert("RGB").save(output_path, quality=95)
    print(f"Created: {output_path}")

def generate_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shots_dir = os.path.join(base_dir, "screenshots")
    
    # -------------------------------------------------------------------------
    # 1. Main Dashboard with Google Maps
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "01_dashboard_google_maps_live.png"),
        output_path=os.path.join(shots_dir, "marked_01_dashboard.png"),
        highlights=[
            {"box": (820, 82, 1340, 136), "num": 1, "color": "#10b981"},
            {"box": (70, 158, 1340, 226), "num": 2, "color": "#f59e0b"},
            {"box": (70, 245, 480, 520), "num": 3, "color": "#0284c7"},
            {"box": (70, 535, 480, 775), "num": 4, "color": "#a855f7"},
            {"box": (495, 245, 1340, 885), "num": 5, "color": "#ef4444"},
        ],
        legend_title="Main GIS Dashboard & Google Maps Integration",
        legend_items=[
            {"num": 1, "title": "Spatial Network Switcher", "desc": "Toggle between 32 Bangladesh Districts (National) and Dhaka Metro (Urban).", "color": "#10b981"},
            {"num": 2, "title": "1-Click Demo Scenarios", "desc": "Pre-configured routes (e.g. Dhaka ➔ Chattogram) for instant testing with zero typing.", "color": "#f59e0b"},
            {"num": 3, "title": "Origin & Target Jela Selectors", "desc": "Pick Origin (Green Pin A) & Destination (Red Pin B) with Division filter.", "color": "#0284c7"},
            {"num": 4, "title": "Algorithm Selector", "desc": "Choose between BFS, DFS, Dijkstra, A*, or Compare All 4 side-by-side.", "color": "#a855f7"},
            {"num": 5, "title": "Google Maps Live API Layer", "desc": "Real Google Maps tiles loaded with verified API key and 32 custom district pins.", "color": "#ef4444"},
        ]
    )

    # -------------------------------------------------------------------------
    # 2. A* Pathfinding Route & Metrics
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "02_a_star_path_google_map.png"),
        output_path=os.path.join(shots_dir, "marked_02_a_star_route.png"),
        highlights=[
            {"box": (500, 30, 1340, 280), "num": 1, "color": "#10b981"},
            {"box": (70, 305, 1340, 445), "num": 2, "color": "#0284c7"},
            {"box": (70, 465, 1340, 890), "num": 3, "color": "#f59e0b"},
        ],
        legend_title="A* Shortest Route & Performance Itinerary",
        legend_items=[
            {"num": 1, "title": "Google Maps Route Polyline", "desc": "Optimal 232.2 km highway path connecting Dhaka ➔ Narayanganj ➔ Cumilla ➔ Feni ➔ Chattogram.", "color": "#10b981"},
            {"num": 2, "title": "Execution Metric Cards", "desc": "Global minimum distance (232.2 km), sub-millisecond latency (0.34 ms), and 24% search space.", "color": "#0284c7"},
            {"num": 3, "title": "Turn-by-Turn Jela Itinerary", "desc": "Complete step-by-step table showing individual segment kilometers and running cumulative totals.", "color": "#f59e0b"},
        ]
    )

    # -------------------------------------------------------------------------
    # 3. Part C 4-Way Comparison Matrix
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "06_four_way_comparison_matrix.png"),
        output_path=os.path.join(shots_dir, "marked_03_four_way_comparison.png"),
        highlights=[
            {"box": (70, 110, 1340, 360), "num": 1, "color": "#0284c7"},
            {"box": (70, 380, 1340, 680), "num": 2, "color": "#10b981"},
            {"box": (70, 700, 1340, 810), "num": 3, "color": "#a855f7"},
        ],
        legend_title="4-Way Algorithm Benchmark Matrix (BFS vs DFS vs Dijkstra vs A*)",
        legend_items=[
            {"num": 1, "title": "4-Way Side-by-Side Benchmark Table", "desc": "Compares Distance (km), Segment Hops, Nodes Explored, and Execution Latency (ms).", "color": "#0284c7"},
            {"num": 2, "title": "Search Space Expansion Progress Bars", "desc": "Visually proves A* examined only 7 Jelas (75.8% search reduction over Dijkstra’s 29 Jelas).", "color": "#10b981"},
            {"num": 3, "title": "Algorithmic Analysis Banner", "desc": "Explains how the Haversine heuristic guides A* directly to goal, and why DFS creates massive detours.", "color": "#a855f7"},
        ]
    )

    # -------------------------------------------------------------------------
    # 4. Projector Day View (Light Theme)
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "07_projector_day_view_google_map.png"),
        output_path=os.path.join(shots_dir, "marked_04_projector_view.png"),
        highlights=[
            {"box": (1040, 12, 1210, 52), "num": 1, "color": "#f59e0b"},
            {"box": (70, 75, 1340, 885), "num": 2, "color": "#0284c7"},
        ],
        legend_title="High-Contrast Projector / Classroom View",
        legend_items=[
            {"num": 1, "title": "One-Click Theme Switcher", "desc": "Toggles between Projector View (Day) and Dashboard View (Night) in top navigation bar.", "color": "#f59e0b"},
            {"num": 2, "title": "WCAG 2.1 AA Compliant Palette", "desc": "Clean white background with dark slate text (>10:1 contrast ratio) preventing projector washout.", "color": "#0284c7"},
        ]
    )

    # -------------------------------------------------------------------------
    # 5. DFS Detour Route
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "05_dfs_deep_detour_route.png"),
        output_path=os.path.join(shots_dir, "marked_05_dfs_detour.png"),
        highlights=[
            {"box": (500, 30, 1340, 280), "num": 1, "color": "#ef4444"},
            {"box": (70, 305, 1340, 445), "num": 2, "color": "#f59e0b"},
        ],
        legend_title="DFS (Depth-First Search) Suboptimal Detour Demonstration",
        legend_items=[
            {"num": 1, "title": "DFS Deep Branch Traversal", "desc": "Explores deep branches across northern & western divisions before finding destination.", "color": "#ef4444"},
            {"num": 2, "title": "Detour Route Metrics", "desc": "Takes 20 Hops and 1,329.6 km (+1,097.4 km detour), demonstrating why DFS is unsuitable for routing.", "color": "#f59e0b"},
        ]
    )

    # -------------------------------------------------------------------------
    # 6. Django Admin Panel
    # -------------------------------------------------------------------------
    create_annotated_image(
        input_path=os.path.join(shots_dir, "09_django_admin_database_models.png"),
        output_path=os.path.join(shots_dir, "marked_06_django_admin.png"),
        highlights=[
            {"box": (50, 60, 1360, 880), "num": 1, "color": "#10b981"},
        ],
        legend_title="Django Administrative Backend for Spatial Models",
        legend_items=[
            {"num": 1, "title": "Django Admin CRUD Interface", "desc": "Allows administrators & evaluators to add, edit, or delete Bangladesh Jelas, Bangla names, and edges.", "color": "#10b981"},
        ]
    )

    print("All marked-up screenshots created with high-clarity legend footers!")

if __name__ == "__main__":
    generate_all()
