import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    try:
        font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def draw_callout(draw, box, badge_num, title_text, color_hex="#ef4444", text_align="top"):
    x1, y1, x2, y2 = box
    r, g, b = int(color_hex[1:3], 16), int(color_hex[3:5], 16), int(color_hex[5:7], 16)
    
    # 1. Draw Bounding Rectangle
    draw.rounded_rectangle([x1, y1, x2, y2], radius=8, outline=(r, g, b, 255), width=3)
    
    # 2. Measure Text & Pill Dimensions
    font_badge = get_font(14, bold=True)
    font_text = get_font(13, bold=True)
    
    bbox = font_text.getbbox(title_text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    pill_h = 28
    badge_w = 28
    pill_w = badge_w + text_w + 20
    
    # Pill position
    if text_align == "top":
        px = max(10, min(x1, 1400 - pill_w))
        py = max(8, y1 - 32)
        if py < 10:
            py = y1 + 6
    else:
        px = max(10, min(x1, 1400 - pill_w))
        py = min(920, y2 + 6)

    # 3. Draw Pill Background
    draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=14, fill=(15, 23, 42, 240), outline=(r, g, b, 255), width=2)
    
    # 4. Draw Circular Number Badge
    badge_cx = px + 14
    badge_cy = py + 14
    draw.ellipse([badge_cx - 11, badge_cy - 11, badge_cx + 11, badge_cy + 11], fill=(r, g, b, 255))
    
    # Number inside badge
    n_str = str(badge_num)
    n_box = font_badge.getbbox(n_str)
    n_w = n_box[2] - n_box[0]
    n_h = n_box[3] - n_box[1]
    draw.text((badge_cx - n_w / 2, badge_cy - n_h / 2 - 2), n_str, fill=(255, 255, 255), font=font_badge)
    
    # 5. Draw Explanatory Text
    draw.text((px + 32, py + 5), title_text, fill=(255, 255, 255), font=font_text)

def annotate_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    shots_dir = os.path.join(base_dir, "screenshots")
    
    # -------------------------------------------------------------
    # 1. Mark Dashboard Screenshot
    # -------------------------------------------------------------
    f1 = os.path.join(shots_dir, "01_dashboard_google_maps_live.png")
    if os.path.exists(f1):
        img1 = Image.open(f1).convert("RGBA")
        d1 = ImageDraw.Draw(img1)
        
        draw_callout(d1, (820, 82, 1340, 136), 1, "Spatial Network Switcher: Toggle Bangladesh 32 Jelas vs Dhaka Metro", "#10b981")
        draw_callout(d1, (70, 158, 1340, 226), 2, "1-Click Demo Presets: Instantly test scenarios with zero typing", "#f59e0b")
        draw_callout(d1, (70, 245, 480, 520), 3, "Route Selectors: Origin (A) & Destination (B) + Division Filter", "#0284c7")
        draw_callout(d1, (70, 535, 480, 775), 4, "Algorithm Selector: BFS, DFS, Dijkstra, A*, or Compare All", "#a855f7")
        draw_callout(d1, (495, 245, 1340, 885), 5, "Live Google Maps API Layer: Verified Key with 32 District Pins", "#ef4444")
        
        out1 = os.path.join(shots_dir, "marked_01_dashboard.png")
        img1.convert("RGB").save(out1, quality=95)
        print(f"Created annotated screenshot: {out1}")

    # -------------------------------------------------------------
    # 2. Mark A* Route Screenshot
    # -------------------------------------------------------------
    f2 = os.path.join(shots_dir, "02_a_star_path_google_map.png")
    if os.path.exists(f2):
        img2 = Image.open(f2).convert("RGBA")
        d2 = ImageDraw.Draw(img2)
        
        draw_callout(d2, (500, 30, 1340, 280), 1, "Google Maps Optimal Route Polyline: Dhaka ➔ Chattogram (232.2 km)", "#10b981")
        draw_callout(d2, (70, 305, 1340, 445), 2, "Real-Time Metric Cards: Distance (232.2 km), Latency (0.34 ms), Search Space (24%)", "#0284c7")
        draw_callout(d2, (70, 465, 1340, 890), 3, "Turn-by-Turn Jela Itinerary Table: Segment & Cumulative Highway Distances", "#f59e0b")
        
        out2 = os.path.join(shots_dir, "marked_02_a_star_route.png")
        img2.convert("RGB").save(out2, quality=95)
        print(f"Created annotated screenshot: {out2}")

    # -------------------------------------------------------------
    # 3. Mark 4-Way Comparison Matrix Screenshot
    # -------------------------------------------------------------
    f3 = os.path.join(shots_dir, "06_four_way_comparison_matrix.png")
    if os.path.exists(f3):
        img3 = Image.open(f3).convert("RGBA")
        d3 = ImageDraw.Draw(img3)
        
        draw_callout(d3, (70, 110, 1340, 360), 1, "Side-by-Side Benchmark Table: BFS vs DFS vs Dijkstra vs A*", "#0284c7")
        draw_callout(d3, (70, 380, 1340, 680), 2, "Search Space Expansion Bars: A* explored only 7 nodes (75.8% search reduction!)", "#10b981")
        draw_callout(d3, (70, 700, 1340, 810), 3, "Heuristic Analysis: Explains why A* prunes and why DFS takes detours (+1,097 km)", "#a855f7")
        
        out3 = os.path.join(shots_dir, "marked_03_four_way_comparison.png")
        img3.convert("RGB").save(out3, quality=95)
        print(f"Created annotated screenshot: {out3}")

    # -------------------------------------------------------------
    # 4. Mark Projector / Day View Screenshot
    # -------------------------------------------------------------
    f4 = os.path.join(shots_dir, "07_projector_day_view_google_map.png")
    if os.path.exists(f4):
        img4 = Image.open(f4).convert("RGBA")
        d4 = ImageDraw.Draw(img4)
        
        draw_callout(d4, (1040, 12, 1210, 52), 1, "One-Click Theme Switcher: Toggles Projector View vs Dashboard View", "#f59e0b")
        draw_callout(d4, (70, 75, 1340, 885), 2, "High-Contrast Projector Palette: >10:1 WCAG contrast ratio prevents projector washout", "#0284c7")
        
        out4 = os.path.join(shots_dir, "marked_04_projector_view.png")
        img4.convert("RGB").save(out4, quality=95)
        print(f"Created annotated screenshot: {out4}")

    # -------------------------------------------------------------
    # 5. Mark DFS Detour Screenshot
    # -------------------------------------------------------------
    f5 = os.path.join(shots_dir, "05_dfs_deep_detour_route.png")
    if os.path.exists(f5):
        img5 = Image.open(f5).convert("RGBA")
        d5 = ImageDraw.Draw(img5)
        
        draw_callout(d5, (500, 30, 1340, 280), 1, "DFS Detour Traversal: Takes deep country-wide detour (+1,097 km excess distance)", "#ef4444")
        draw_callout(d5, (70, 305, 1340, 445), 2, "Suboptimal Routing Metrics: 20 Hops, 1,329.6 km (Proof DFS is unsuitable for routing)", "#f59e0b")
        
        out5 = os.path.join(shots_dir, "marked_05_dfs_detour.png")
        img5.convert("RGB").save(out5, quality=95)
        print(f"Created annotated screenshot: {out5}")

    # -------------------------------------------------------------
    # 6. Mark Django Admin Screenshot
    # -------------------------------------------------------------
    f6 = os.path.join(shots_dir, "09_django_admin_database_models.png")
    if os.path.exists(f6):
        img6 = Image.open(f6).convert("RGBA")
        d6 = ImageDraw.Draw(img6)
        
        draw_callout(d6, (50, 60, 1360, 880), 1, "Django Admin Panel: Full CRUD management for Bangladesh Jelas, Coordinates & Edges", "#10b981")
        
        out6 = os.path.join(shots_dir, "marked_06_django_admin.png")
        img6.convert("RGB").save(out6, quality=95)
        print(f"Created annotated screenshot: {out6}")

    print("All markable screenshots annotated successfully!")

if __name__ == "__main__":
    annotate_all()
