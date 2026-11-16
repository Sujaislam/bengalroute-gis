import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    try:
        font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def create_annotated_image(input_path, output_path, highlights, legend_items):
    """
    input_path: path to base screenshot (1410 x 958)
    highlights: list of dicts: [
        {"box": (x1, y1, x2, y2), "num": 1, "color": "#ef4444"}, ...
    ]
    legend_items: list of dicts: [
        {"num": 1, "title": "Network Switcher", "desc": "Toggle between 32 Bangladesh Districts and Dhaka Metro", "color": "#ef4444"}, ...
    ]
    """
    base_img = Image.open(input_path).convert("RGBA")
    w, h = base_img.size

    # Add 220px bottom legend banner for crystal-clear readability
    legend_h = 220
    new_h = h + legend_h
    canvas = Image.new("RGBA", (w, new_h), (15, 23, 42, 255)) # Dark slate-950
    canvas.paste(base_img, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # 1. Draw Highlights on Screenshot Area
    font_badge = get_font(18, bold=True)
    
    for item in highlights:
        x1, y1, x2, y2 = item["box"]
        col_hex = item["color"]
        r, g, b = int(col_hex[1:3], 16), int(col_hex[3:5], 16), int(col_hex[5:7], 16)
        
        # Outer glow/border
        draw.rounded_rectangle([x1 - 1, y1 - 1, x2 + 1, y2 + 1], radius=6, outline=(255, 255, 255, 180), width=1)
        # Main thick border
        draw.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=(r, g, b, 255), width=4)

        # Large Circular Number Badge (34px diameter)
        badge_r = 18
        bx = x1 + 16
        by = y1 + 16
        # White drop outline
        draw.ellipse([bx - badge_r - 2, by - badge_r - 2, bx + badge_r + 2, by + badge_r + 2], fill=(255, 255, 255, 255))
        # Solid colored circle
        draw.ellipse([bx - badge_r, by - badge_r, bx + badge_r, by + badge_r], fill=(r, g, b, 255))
        
        # Number text
        n_str = str(item["num"])
        bbox = font_badge.getbbox(n_str)
        nw = bbox[2] - bbox[0]
        nh = bbox[3] - bbox[1]
        draw.text((bx - nw / 2, by - nh / 2 - 2), n_str, fill=(255, 255, 255), font=font_badge)

    # 2. Draw Legend Divider
    draw.line([(0, h), (w, h)], fill=(51, 65, 85, 255), width=3) # Slate-700
    
    # Legend Header
    font_legend_hdr = get_font(14, bold=True)
    draw.text((25, h + 12), "📌 SCREENSHOT FEATURE EXPLANATION & CALLOUT GUIDE:", fill=(245, 158, 11, 255), font=font_legend_hdr)

    # 3. Draw Legend Items (2 Columns for generous spacing and large readable text)
    font_title = get_font(14, bold=True)
    font_desc = get_font(13, bold=False)
    
    col1_x = 25
    col2_x = 720
    start_y = h + 42
    row_h = 52

    for idx, leg in enumerate(legend_items):
        col_x = col1_x if idx < 3 else col2_x
        row_idx = idx if idx < 3 else idx - 3
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

        # Legend Title & Description
        draw.text((col_x + 38, curr_y), leg["title"], fill=(255, 255, 255), font=font_title)
        draw.text((col_x + 38, curr_y + 20), leg["desc"], fill=(203, 213, 225), font=font_desc) # Slate-300

    # Save Image
    canvas.convert("RGB").save(output_path, quality=95)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    base = r"C:\Users\suja\map_pathfinder\screenshots"
    in_img = os.path.join(base, "01_dashboard_google_maps_live.png")
    out_img = os.path.join(base, "marked_01_dashboard.png")

    hls = [
        {"box": (820, 82, 1340, 136), "num": 1, "color": "#10b981"},
        {"box": (70, 158, 1340, 226), "num": 2, "color": "#f59e0b"},
        {"box": (70, 245, 480, 520), "num": 3, "color": "#0284c7"},
        {"box": (70, 535, 480, 775), "num": 4, "color": "#a855f7"},
        {"box": (495, 245, 1340, 885), "num": 5, "color": "#ef4444"},
    ]

    legs = [
        {"num": 1, "title": "Spatial Network Switcher", "desc": "Toggle between 32 Bangladesh Districts (National) and Dhaka Metro (Urban).", "color": "#10b981"},
        {"num": 2, "title": "1-Click Presentation Presets", "desc": "Click any scenario (e.g. Dhaka ➔ Chattogram) to auto-configure & run.", "color": "#f59e0b"},
        {"num": 3, "title": "Origin & Target Jela Selectors", "desc": "Choose origin (Green Pin A) & destination (Red Pin B) with Division filter.", "color": "#0284c7"},
        {"num": 4, "title": "Pathfinding Algorithm Engine", "desc": "Select BFS, DFS, Dijkstra, A*, or Compare All 4 side-by-side.", "color": "#a855f7"},
        {"num": 5, "title": "Live Google Maps API Layer", "desc": "Satellite/Street map rendered with verified API key and 32 custom Jela pins.", "color": "#ef4444"},
    ]

    create_annotated_image(in_img, out_img, hls, legs)
