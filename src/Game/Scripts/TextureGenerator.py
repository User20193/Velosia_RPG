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

def generate_grass(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (40, 140, 40, 255))
    pixels = img.load()

    # Strict pixel-art blades of grass
    # Draw small "V" or "l" shapes in a rigid grid for a clean tile look
    shade_dark = (20, 100, 20, 255)
    shade_light = (60, 180, 60, 255)

    for y in range(0, height, 8):
        for x in range(0, width, 8):
            # Offset every other row
            ox = x + (4 if (y // 8) % 2 != 0 else 0)
            if ox >= width: continue

            # Draw a pixel blade
            pixels[ox, y+4] = shade_dark
            pixels[ox, y+3] = shade_light
            pixels[ox, y+2] = shade_light
            if ox+1 < width:
                pixels[ox+1, y+3] = shade_dark

    img.save(output_path)
    print(f"Generated grass at {output_path}")

def generate_tree(output_path):
    width, height = 64, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Pixel-art tree using blocky layered rectangles
    trunk_color = (100, 50, 20, 255)
    trunk_shadow = (70, 30, 10, 255)

    leaf_dark = (10, 80, 10, 255)
    leaf_mid = (20, 120, 20, 255)
    leaf_light = (40, 160, 40, 255)

    # Trunk
    draw.rectangle([28, 40, 36, 60], fill=trunk_color)
    draw.rectangle([28, 40, 32, 60], fill=trunk_shadow) # Shading on trunk

    # Base roots
    draw.rectangle([24, 58, 40, 62], fill=trunk_color)
    draw.rectangle([24, 58, 28, 62], fill=trunk_shadow)

    # Canopy (blocky)
    # Bottom layer
    draw.rectangle([12, 32, 52, 48], fill=leaf_dark)
    # Mid layer
    draw.rectangle([16, 16, 48, 38], fill=leaf_mid)
    # Top layer
    draw.rectangle([22, 6, 42, 22], fill=leaf_light)

    # Add some chunky "leaves" detail
    pixels = img.load()
    for y in range(16, 48, 4):
        for x in range(16, 48, 4):
            if pixels[x, y] == leaf_mid:
                draw.rectangle([x, y, x+2, y+2], fill=leaf_dark)

    img.save(output_path)
    print(f"Generated tree at {output_path}")

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

    generate_grass('assets/textures/grass.png')
    generate_tree('assets/textures/tree.png')
    generate_player('assets/textures/player_idle.png')
