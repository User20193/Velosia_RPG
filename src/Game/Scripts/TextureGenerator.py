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
    img = Image.new("RGBA", (width, height), (34, 139, 34, 255)) # Forest Green base
    draw = ImageDraw.Draw(img)

    # Add some noise/blades of grass
    for _ in range(30):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        shade = random.choice([(0, 100, 0, 255), (50, 205, 50, 255), (0, 128, 0, 255)])
        draw.point((x, y), fill=shade)
        if y > 0:
            draw.point((x, y-1), fill=shade)

    img.save(output_path)
    print(f"Generated grass at {output_path}")

def generate_tree(output_path):
    width, height = 64, 96
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Trunk
    trunk_color = (139, 69, 19, 255) # Saddle Brown
    draw.rectangle([24, 64, 40, 90], fill=trunk_color)

    # Leaves (3/4 top-down perspective, overlapping circles)
    leaf_color_dark = (0, 100, 0, 255)
    leaf_color_light = (34, 139, 34, 255)

    # Draw bottom layer
    draw.ellipse([8, 40, 56, 80], fill=leaf_color_dark)
    # Draw top layer
    draw.ellipse([16, 16, 48, 64], fill=leaf_color_light)
    # Highlight
    draw.ellipse([24, 24, 40, 40], fill=(50, 205, 50, 255))

    img.save(output_path)
    print(f"Generated tree at {output_path}")

def generate_player(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Shadow
    draw.ellipse([8, 26, 24, 30], fill=(0, 0, 0, 100))

    # Body (Blue tunic)
    draw.rectangle([10, 14, 22, 28], fill=(65, 105, 225, 255))

    # Head
    draw.ellipse([10, 4, 22, 16], fill=(255, 218, 185, 255)) # Peach/skin tone

    # Eyes (looking down/forward for 3/4 perspective)
    draw.point((13, 10), fill=(0, 0, 0, 255))
    draw.point((18, 10), fill=(0, 0, 0, 255))

    # Arms
    draw.rectangle([6, 14, 10, 22], fill=(65, 105, 225, 255))
    draw.rectangle([22, 14, 26, 22], fill=(65, 105, 225, 255))

    # Hands
    draw.rectangle([6, 22, 10, 24], fill=(255, 218, 185, 255))
    draw.rectangle([22, 22, 26, 24], fill=(255, 218, 185, 255))

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
