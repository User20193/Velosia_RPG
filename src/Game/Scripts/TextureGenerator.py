import os
import random
import math
from PIL import Image, ImageDraw

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def generate_stone_wall(output_path):
    """
    Generates a 32x32 seamless procedural pixel-art stone wall.
    Uses a grid approach with perturbed vertices and fake directional lighting.
    """
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    pixels = img.load()

    # Fantasy Dark Stone Palette (dark to light)
    base_color = (43, 45, 66)
    highlight_color = (141, 153, 174)
    shadow_color = (20, 22, 35)
    mortar_color = (10, 11, 15)

    # We'll create a 2x4 grid of stones to make it seamless on a 32x32 texture
    # Columns = 2 (16px each), Rows = 4 (8px each)
    cols = 2
    rows = 4

    col_width = width // cols
    row_height = height // rows

    # Create a base map for stone IDs to track which pixel belongs to which stone
    stone_map = [[-1 for _ in range(height)] for _ in range(width)]

    # Perturb the grid to make stones look natural, but keep edges wrap-around
    # We define horizontal lines and vertical dividers
    # Row 0: y=0, Row 1: y=8, Row 2: y=16, Row 3: y=24
    # To make it brick-like, odd rows are shifted.

    for y in range(height):
        for x in range(width):
            # Determine base row and col
            r = y // row_height

            # Stagger every other row
            shift = (col_width // 2) if r % 2 != 0 else 0

            # Add some noise to the boundaries
            noise_x = int(math.sin(y * 1.5) * 1.5)
            noise_y = int(math.cos(x * 1.5) * 1.5)

            eff_x = (x + shift + noise_x) % width
            eff_y = (y + noise_y) % height

            c = eff_x // col_width

            # Boundary detection for mortar
            # Are we near the edge of a cell?
            rem_x = eff_x % col_width
            rem_y = eff_y % row_height

            # Thick mortar
            if rem_x < 2 or rem_x > col_width - 2 or rem_y < 2 or rem_y > row_height - 2:
                stone_map[x][y] = -1 # Mortar
            else:
                stone_map[x][y] = (r * cols) + c

    # Now color the pixels based on the map and apply lighting
    for y in range(height):
        for x in range(width):
            s_id = stone_map[x][y]
            if s_id == -1:
                # Mortar
                pixels[x, y] = mortar_color
            else:
                # Stone body
                # Basic noise for texture
                noise = random.randint(-5, 5)
                r_base, g_base, b_base = base_color

                # Check neighbors for bevel lighting
                # Top/Left neighbors
                is_top_edge = stone_map[x][(y-1)%height] == -1
                is_left_edge = stone_map[(x-1)%width][y] == -1

                # Bottom/Right neighbors
                is_bottom_edge = stone_map[x][(y+1)%height] == -1
                is_right_edge = stone_map[(x+1)%width][y] == -1

                if is_top_edge or is_left_edge:
                    # Highlight
                    r, g, b = highlight_color
                    pixels[x, y] = (r + noise, g + noise, b + noise, 255)
                elif is_bottom_edge or is_right_edge:
                    # Shadow
                    r, g, b = shadow_color
                    pixels[x, y] = (r + noise, g + noise, b + noise, 255)
                else:
                    # Base
                    pixels[x, y] = (r_base + noise, g_base + noise, b_base + noise, 255)

    img.save(output_path)
    print(f"Generated stone wall at {output_path}")

def generate_liana(output_path):
    """
    Generates a 32x64 procedural liana (vine) sprite.
    Uses a random walk algorithm with branching for leaves.
    Transparent background.
    """
    width, height = 32, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0)) # Fully transparent
    draw = ImageDraw.Draw(img)

    base_color = (34, 139, 34, 255)     # Forest Green
    highlight_color = (50, 205, 50, 255)# Lime Green
    outline_color = (0, 50, 0, 255)     # Dark outline

    # Start at top center
    x = width // 2
    y = 0

    # Store the main vine path
    path = []

    while y < height - 2:
        path.append((x, y))

        # Move down, and randomly wander left or right slightly
        y += 1
        x += random.choice([-1, 0, 0, 1]) # Slight bias to stay center

        # Keep inside bounds
        x = clamp(x, 2, width - 3)

    # Draw Outline first (thicker)
    for px, py in path:
        draw.ellipse([px-2, py-1, px+2, py+1], fill=outline_color)

    # Draw Base color
    for px, py in path:
        draw.ellipse([px-1, py, px+1, py], fill=base_color)

    # Draw Highlight (left side)
    for px, py in path:
        img.putpixel((px-1, py), highlight_color)

    # Add random leaves
    for px, py in path:
        if random.random() < 0.15 and py < height - 5: # 15% chance per pixel to sprout a leaf
            side = random.choice([-1, 1])
            leaf_x = px + side * 3
            leaf_y = py + 2

            # Leaf outline
            draw.point((leaf_x, leaf_y), fill=outline_color)
            draw.point((leaf_x + side, leaf_y), fill=outline_color)
            draw.point((leaf_x, leaf_y - 1), fill=outline_color)

            # Leaf fill
            draw.point((leaf_x, leaf_y), fill=highlight_color)

    img.save(output_path)
    print(f"Generated liana at {output_path}")

if __name__ == "__main__":
    os.makedirs('assets/textures', exist_ok=True)
    generate_stone_wall('assets/textures/wall_bg.png')
    generate_liana('assets/textures/liana.png')
