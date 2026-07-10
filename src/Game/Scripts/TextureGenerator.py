import os
import random
import math
from PIL import Image, ImageDraw

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def generate_stone_wall(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    pixels = img.load()
    base_color = (25, 27, 33)
    alt_color = (20, 22, 28)
    for y in range(height):
        for x in range(width):
            if (x + y) % 2 == 0:
                pixels[x, y] = base_color
            else:
                pixels[x, y] = alt_color
    img.save(output_path)
    print(f"Generated minimal background at {output_path}")

def generate_liana(output_path, length=64, base_color=(0, 200, 100, 255)):
    width, height = 32, length
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    highlight_color = (50, 255, 150, 255)
    outline_color = (0, 40, 20, 255)

    x = width // 2
    y = 0
    path = []

    while y < height - 2:
        path.append((x, y))
        y += 1
        x += random.choice([-1, 0, 0, 1])
        x = clamp(x, 2, width - 3)

    for px, py in path:
        draw.ellipse([px-2, py-1, px+2, py+1], fill=outline_color)
    for px, py in path:
        draw.ellipse([px-1, py, px+1, py], fill=base_color)
    for px, py in path:
        img.putpixel((px-1, py), highlight_color)

    for px, py in path:
        if random.random() < 0.15 and py < height - 5:
            side = random.choice([-1, 1])
            leaf_x = px + side * 3
            leaf_y = py + 2
            draw.point((leaf_x, leaf_y), fill=outline_color)
            draw.point((leaf_x + side, leaf_y), fill=outline_color)
            draw.point((leaf_x, leaf_y - 1), fill=outline_color)
            draw.point((leaf_x, leaf_y), fill=highlight_color)

    img.save(output_path)
    print(f"Generated liana at {output_path}")

def generate_fog(output_path):
    width, height = 1366, 256
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    pixels = img.load()

    for y in range(height):
        # Create a gradient for the fog: more opaque at the bottom, fully transparent at the top
        alpha = int((y / height) * 200) # Max alpha 200
        # Color: deep bluish-gray fog
        color = (30, 40, 50, alpha)
        for x in range(width):
            # We can add some slight horizontal noise or just leave it as a gradient
            pixels[x, y] = color

    img.save(output_path)
    print(f"Generated fog at {output_path}")

def fill_circle_pixels(draw, cx, cy, r, color):
    # A helper to draw filled circles in a strict pixel-art fashion (no anti-aliasing)
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x*x + y*y <= r*r:
                draw.point((cx + x, cy + y), fill=color)

def generate_grass_variant(output_path, variant="base"):
    width, height = 32, 32

    # Base fantasy grass color
    base_color = (60, 150, 70, 255)
    img = Image.new("RGBA", (width, height), base_color)
    draw = ImageDraw.Draw(img)

    # Noise/texture colors
    highlight = (80, 175, 90, 255)
    shadow = (40, 120, 50, 255)
    deep_shadow = (25, 95, 35, 255)

    # Sprinkle some organic pixel clusters for texture
    random.seed(variant + output_path) # Deterministic for consistent generation
    for _ in range(15):
        x = random.randint(0, width - 2)
        y = random.randint(0, height - 2)
        draw.point((x, y), fill=shadow)
        draw.point((x+1, y), fill=deep_shadow)
        draw.point((x, y+1), fill=highlight)

    if variant == "flower":
        # Add a tiny 3x3 flower
        fx, fy = random.randint(4, 28), random.randint(4, 28)
        flower_center = (255, 200, 0, 255)
        flower_petal = (200, 200, 255, 255)
        # Petals (cross)
        draw.point((fx-1, fy), fill=flower_petal)
        draw.point((fx+1, fy), fill=flower_petal)
        draw.point((fx, fy-1), fill=flower_petal)
        draw.point((fx, fy+1), fill=flower_petal)
        # Center
        draw.point((fx, fy), fill=flower_center)

    elif variant == "stone":
        # Small grey stone cluster
        sx, sy = random.randint(4, 24), random.randint(4, 24)
        stone_light = (160, 160, 170, 255)
        stone_dark = (100, 100, 110, 255)
        stone_shadow = (60, 60, 70, 255)

        draw.rectangle([sx, sy, sx+3, sy+2], fill=stone_light)
        draw.rectangle([sx, sy+2, sx+3, sy+3], fill=stone_dark)
        draw.rectangle([sx+3, sy, sx+4, sy+3], fill=stone_shadow)

    img.save(output_path)
    print(f"Generated {variant} grass at {output_path}")

def generate_tree_oak(output_path):
    width, height = 64, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Fantasy Oak colors
    trunk_color = (110, 70, 40, 255)
    trunk_shadow = (75, 45, 25, 255)
    trunk_highlight = (140, 95, 60, 255)

    leaf_deep = (10, 65, 30, 255)
    leaf_shadow = (20, 90, 40, 255)
    leaf_base = (35, 125, 55, 255)
    leaf_highlight = (65, 165, 80, 255)

    # Trunk
    draw.rectangle([28, 40, 36, 60], fill=trunk_color)
    draw.rectangle([28, 40, 30, 60], fill=trunk_highlight)
    draw.rectangle([34, 40, 36, 60], fill=trunk_shadow)

    # Roots
    draw.rectangle([24, 58, 28, 61], fill=trunk_shadow)
    draw.rectangle([36, 58, 40, 61], fill=trunk_shadow)

    # Canopy (Organic Pixel Clusters)
    # We draw circles starting from back/shadow to front/highlight
    # Deep shadow base
    fill_circle_pixels(draw, 32, 28, 22, leaf_deep)
    fill_circle_pixels(draw, 22, 34, 14, leaf_deep)
    fill_circle_pixels(draw, 42, 34, 14, leaf_deep)

    # Base color
    fill_circle_pixels(draw, 32, 26, 20, leaf_base)
    fill_circle_pixels(draw, 22, 32, 12, leaf_base)
    fill_circle_pixels(draw, 42, 32, 12, leaf_base)

    # Shadows underneath clusters
    fill_circle_pixels(draw, 32, 32, 16, leaf_shadow)
    fill_circle_pixels(draw, 22, 36, 10, leaf_shadow)
    fill_circle_pixels(draw, 42, 36, 10, leaf_shadow)

    # Highlights on top of clusters
    fill_circle_pixels(draw, 28, 18, 12, leaf_highlight)
    fill_circle_pixels(draw, 38, 22, 10, leaf_highlight)
    fill_circle_pixels(draw, 20, 26, 8, leaf_highlight)

    img.save(output_path)
    print(f"Generated Oak Tree at {output_path}")

def generate_tree_pine(output_path):
    width, height = 64, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    trunk_color = (90, 60, 40, 255)
    trunk_shadow = (60, 35, 20, 255)

    leaf_deep = (10, 50, 40, 255)
    leaf_shadow = (15, 75, 60, 255)
    leaf_base = (25, 105, 80, 255)
    leaf_highlight = (45, 135, 100, 255)

    # Trunk
    draw.rectangle([30, 50, 34, 62], fill=trunk_color)
    draw.rectangle([32, 50, 34, 62], fill=trunk_shadow)

    # Pine cones / triangular layers
    def draw_pine_layer(y_top, w, color):
        for y in range(16):
            # Calculate width at this y
            cur_w = int((y / 16.0) * w)
            draw.line((32 - cur_w, y_top + y, 32 + cur_w, y_top + y), fill=color)

    # Draw bottom to top
    # Layer 1 (Bottom)
    draw_pine_layer(36, 24, leaf_deep)
    draw_pine_layer(34, 22, leaf_base)
    draw_pine_layer(32, 18, leaf_highlight)

    # Layer 2 (Mid)
    draw_pine_layer(24, 20, leaf_shadow)
    draw_pine_layer(22, 18, leaf_base)
    draw_pine_layer(20, 14, leaf_highlight)

    # Layer 3 (Top)
    draw_pine_layer(12, 14, leaf_shadow)
    draw_pine_layer(10, 12, leaf_base)
    draw_pine_layer(8, 8, leaf_highlight)

    img.save(output_path)
    print(f"Generated Pine Tree at {output_path}")

def generate_player(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Shadow
    draw.ellipse([8, 26, 24, 30], fill=(0, 0, 0, 100))

    # Strict pixel-art character (16x24 size roughly)
    skin = (255, 200, 150, 255)
    hair = (100, 50, 20, 255)
    shirt = (50, 100, 200, 255)
    shirt_shadow = (30, 60, 150, 255)
    pants = (50, 50, 50, 255)
    shoes = (30, 20, 10, 255)
    outline = (0, 0, 0, 255)

    # Head (10x10)
    draw.rectangle([11, 4, 21, 14], fill=skin, outline=outline)

    # Hair
    draw.rectangle([10, 2, 22, 6], fill=hair, outline=outline)
    draw.rectangle([10, 6, 12, 10], fill=hair)
    draw.rectangle([20, 6, 22, 10], fill=hair)

    # Eyes (2x2)
    draw.rectangle([13, 9, 14, 10], fill=outline)
    draw.rectangle([18, 9, 19, 10], fill=outline)

    # Body (12x10)
    draw.rectangle([10, 15, 22, 23], fill=shirt, outline=outline)
    draw.rectangle([16, 15, 22, 23], fill=shirt_shadow) # Shading on right side

    # Belt
    draw.rectangle([10, 22, 22, 23], fill=(150, 100, 50, 255), outline=outline)
    draw.rectangle([15, 21, 17, 23], fill=(200, 200, 50, 255)) # Belt buckle

    # Left Arm
    draw.rectangle([6, 15, 9, 21], fill=shirt, outline=outline)
    draw.rectangle([6, 21, 9, 23], fill=skin, outline=outline) # Hand

    # Right Arm
    draw.rectangle([23, 15, 26, 21], fill=shirt_shadow, outline=outline)
    draw.rectangle([23, 21, 26, 23], fill=skin, outline=outline) # Hand

    # Left Leg
    draw.rectangle([11, 24, 15, 27], fill=pants, outline=outline)
    draw.rectangle([11, 28, 15, 29], fill=shoes, outline=outline)

    # Right Leg
    draw.rectangle([17, 24, 21, 27], fill=pants, outline=outline)
    draw.rectangle([17, 28, 21, 29], fill=shoes, outline=outline)

    img.save(output_path)
    print(f"Generated player at {output_path}")

if __name__ == "__main__":
    os.makedirs('assets/textures', exist_ok=True)
    generate_stone_wall('assets/textures/wall_bg.png')

    # Generate variations of lianas
    generate_liana('assets/textures/liana_64.png', length=64, base_color=(0, 200, 100, 255))
    generate_liana('assets/textures/liana_128.png', length=128, base_color=(0, 180, 90, 255))
    generate_liana('assets/textures/liana_256.png', length=256, base_color=(0, 150, 80, 255))
    generate_liana('assets/textures/liana_384.png', length=384, base_color=(0, 120, 60, 255))

    generate_fog('assets/textures/fog.png')

    generate_grass_variant('assets/textures/grass_base.png', "base")
    generate_grass_variant('assets/textures/grass_flower.png', "flower")
    generate_grass_variant('assets/textures/grass_stone.png', "stone")

    generate_tree_oak('assets/textures/tree_oak.png')
    generate_tree_pine('assets/textures/tree_pine.png')

    generate_player('assets/textures/player_idle.png')
