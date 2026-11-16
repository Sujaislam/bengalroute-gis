import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=True):
    try:
        font_path = "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

def draw_tabbed_box(draw, x1, y1, x2, y2, color_hex, badge_num, badge_title, font_tab):
    """
    Draws a crisp border around (x1, y1, x2, y2) and a header tab on top-left of the box.
    """
    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)
    border_col = (r, g, b, 255)

    # Outer contrast glow
    draw.rounded_rectangle([x1 - 1, y1 - 1, x2 + 1, y2 + 1], radius=6, outline=(255, 255, 255, 200), width=1)
    # Main thick colored border
    draw.rounded_rectangle([x1, y1, x2, y2], radius=6, outline=border_col, width=3)

    # Header Tab sitting on top-left of the box
    tab_text = f" [{badge_num}]  {badge_title.upper()} "
    bbox = font_tab.getbbox(tab_text)
    tw = (bbox[2] - bbox[0]) + 16
    th = (bbox[3] - bbox[1]) + 10

    # If y1 is very close to top of screen, place tab slightly inside
    tab_y1 = y1 - th + 2 if y1 > th + 5 else y1 + 2
    tab_y2 = tab_y1 + th
    tab_x1 = x1 + 8
    tab_x2 = tab_x1 + tw

    # Tab background
    draw.rounded_rectangle([tab_x1, tab_y1, tab_x2, tab_y2], radius=5, fill=border_col, outline=(255, 255, 255, 220), width=1)
    
    # Tab text (white bold, high contrast)
    draw.text((tab_x1 + 8, tab_y1 + 4), tab_text, fill=(255, 255, 255), font=font_tab)

def annotate_image(base_img_path, output_path, highlights, legend_title, legend_items):
    base_img = Image.open(base_img_path).convert("RGBA")
    w, h = base_img.size

    # Calculate legend height dynamically
    rows = (len(legend_items) + 1) // 2
    legend_h = max(220, 60 + rows * 56)
    canvas = Image.new("RGBA", (w, h + legend_h), (15, 23, 42, 255))
    canvas.paste(base_img, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # Fonts
    font_tab = get_font(13, bold=True)
    font_hdr = get_font(15, bold=True)
    font_leg_title = get_font(13, bold=True)
    font_leg_desc = get_font(12, bold=False)
    font_badge = get_font(12, bold=True)

    # 1. Draw all tabbed boxes on screenshot
    for h_item in highlights:
        x1, y1, x2, y2 = h_item["box"]
        draw_tabbed_box(
            draw=draw,
            x1=x1, y1=y1, x2=x2, y2=y2,
            color_hex=h_item["color"],
            badge_num=h_item["num"],
            badge_title=h_item["title"],
            font_tab=font_tab
        )

    # 2. Draw Legend Divider
    draw.line([(0, h), (w, h)], fill=(71, 85, 105, 255), width=3)
    
    # Legend Header Bar
    draw.rectangle([(0, h), (w, h + 38)], fill=(30, 41, 59, 255))
    draw.text((25, h + 10), f"📌 WHAT THIS SCREENSHOT DEMONSTRATES: {legend_title.upper()}", fill=(245, 158, 11, 255), font=font_hdr)

    # 3. Draw Legend Items in 2 Columns
    col1_x = 25
    col2_x = int(w / 2) + 15
    start_y = h + 48
    row_h = 54

    for idx, leg in enumerate(legend_items):
        col_x = col1_x if idx % 2 == 0 else col2_x
        row_idx = idx // 2
        curr_y = start_y + (row_idx * row_h)

        col_hex = leg["color"]
        r = int(col_hex[1:3], 16)
        g = int(col_hex[3:5], 16)
        b = int(col_hex[5:7], 16)

        # Number Badge
        draw.rounded_rectangle([col_x, curr_y + 2, col_x + 28, curr_y + 26], radius=4, fill=(r, g, b, 255), outline=(255, 255, 255, 200), width=1)
        num_str = str(leg["num"])
        nb_bbox = font_badge.getbbox(num_str)
        nw = nb_bbox[2] - nb_bbox[0]
        nh = nb_bbox[3] - nb_bbox[1]
        draw.text((col_x + 14 - nw/2, curr_y + 14 - nh/2 - 1), num_str, fill=(255, 255, 255), font=font_badge)

        # Title & Description
        draw.text((col_x + 36, curr_y), leg["title"], fill=(255, 255, 255), font=font_leg_title)
        draw.text((col_x + 36, curr_y + 20), leg["desc"], fill=(203, 213, 225), font=font_leg_desc)

    canvas.convert("RGB").save(output_path, quality=95)
    print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    print("Test annotation ready.")
