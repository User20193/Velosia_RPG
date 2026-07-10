import os
import random
import math
from PIL import Image, ImageDraw

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def generate_stone_wall(output_path):
    """
    Generates a 32x32 minimalist background.
    Dark slate with a very faint grid/dithering so it isn't completely flat.
    """
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    pixels = img.load()

    # Minimalist Dark Palette
    base_color = (25, 27, 33)   # Deep slate
    alt_color = (20, 22, 28)    # Slightly darker

    for y in range(height):
        for x in range(width):
            # Extremely subtle checkerboard/dither for minimalist texture
            if (x + y) % 2 == 0:
                pixels[x, y] = base_color
            else:
                pixels[x, y] = alt_color

    img.save(output_path)
    print(f"Generated minimal background at {output_path}")

def generate_liana(output_path):
    """
    Generates a 32x64 procedural liana (vine) sprite.
    Uses a random walk algorithm with branching for leaves.
    Transparent background.
    """
    width, height = 32, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0)) # Fully transparent
    draw = ImageDraw.Draw(img)

    base_color = (0, 200, 100, 255)     # Vibrant Emerald/Mint Green
    highlight_color = (50, 255, 150, 255)# Bright Lime/Mint
    outline_color = (0, 40, 20, 255)     # Very dark green outline

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
