import os
from PIL import Image, ImageDraw
import random

def create_sky(width, height, path):
    img = Image.new('RGBA', (width, height), (15, 15, 30, 255))
    draw = ImageDraw.Draw(img)
    # Gradient
    for y in range(height):
        r = int(15 + (40 * (y / height)))
        g = int(15 + (20 * (y / height)))
        b = int(30 + (40 * (y / height)))
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Stars
    for _ in range(100):
        x = random.randint(0, width - 1)
        y = random.randint(0, height // 2)
        bright = random.randint(150, 255)
        draw.point((x, y), fill=(bright, bright, bright, 255))

    img.save(path)

def create_mountains(width, height, path):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Mountains base
    base_y = int(height * 0.6)

    points = [(0, base_y)]
    segments = 6
    segment_width = width // segments

    # Generate midpoints
    heights = [base_y]
    for i in range(1, segments):
        heights.append(base_y - random.randint(50, 200))
    heights.append(base_y)

    for x in range(width):
        idx = x // segment_width
        if idx >= segments:
            idx = segments - 1

        progress = (x % segment_width) / segment_width

        h = heights[idx] + (heights[idx+1] - heights[idx]) * progress
        h += random.randint(-2, 2)

        draw.line([(x, int(h)), (x, height)], fill=(45, 45, 70, 255))

        if (progress < 0.5):
            draw.point((x, int(h)), fill=(70, 70, 100, 255))

    img.save(path)

def create_forest(width, height, path):
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    base_y = int(height * 0.8)
    draw.rectangle([0, base_y, width, height], fill=(15, 25, 20, 255))

    for i in range(15):
        x = random.randint(20, width - 20)
        tree_w = random.randint(20, 40)
        tree_h = random.randint(100, 250)
        trunk_w = tree_w // 3

        draw.rectangle([x - trunk_w//2, base_y - tree_h//4, x + trunk_w//2, base_y], fill=(30, 20, 15, 255))

        leaf_base = base_y - tree_h // 5
        for j in range(3):
            top_y = base_y - tree_h + (j * 30)
            bot_y = leaf_base - (j * 20)
            w = tree_w - (j * 5)
            draw.polygon([
                (x, top_y),
                (x - w, bot_y),
                (x + w, bot_y)
            ], fill=(20, 50 + (j*10), 30, 255))

    img.save(path)

os.makedirs('assets/textures', exist_ok=True)
create_sky(1366, 768, 'assets/textures/bg_layer1.png')
create_mountains(1366, 768, 'assets/textures/bg_layer2.png')
create_forest(1366, 768, 'assets/textures/bg_layer3.png')
print("Assets generated successfully!")
