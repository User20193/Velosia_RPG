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

def draw_ascii_matrix(draw, matrix, palette, offset_x=0, offset_y=0, scale=1):
    for y, row in enumerate(matrix):
        for x, char in enumerate(row):
            if char in palette:
                color = palette[char]
                px = offset_x + (x * scale)
                py = offset_y + (y * scale)
                if scale == 1:
                    draw.point((px, py), fill=color)
                else:
                    draw.rectangle([px, py, px + scale - 1, py + scale - 1], fill=color)

def generate_tileset(output_path):
    # Generates a 96x32 tileset containing: [0] Grass Base, [1] Grass Flower, [2] Dirt Path
    width, height = 96, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # JRPG Palette (Softer, slightly desaturated)
    P = {
        '.': (128, 184, 114, 255), # Grass Base
        ',': (109, 163,  95, 255), # Grass Detail 1
        ';': ( 89, 140,  76, 255), # Grass Detail 2 (Darker)
        'w': (250, 250, 240, 255), # White Flower
        'p': (230, 160, 200, 255), # Pink Flower
        'y': (240, 210,  80, 255), # Yellow Flower Center
        'd': (186, 148, 108, 255), # Dirt Base (Sand/Soil)
        'D': (163, 126,  88, 255), # Dirt Shadow
        'l': (212, 175, 133, 255), # Dirt Highlight
        'r': (140, 140, 140, 255), # Small pebbles
    }

    def draw_grass_patch(cx, cy):
        # Draw a small tuft of grass
        draw.point((cx, cy), fill=P[';'])
        draw.point((cx-1, cy), fill=P[','])
        draw.point((cx+1, cy), fill=P[','])
        draw.point((cx, cy-1), fill=P[','])

    def fill_grass(offset_x):
        # Fill base
        draw.rectangle([offset_x, 0, offset_x + 31, 31], fill=P['.'])
        # Add soft noise and grass tufts
        for y in range(32):
            for x in range(32):
                if random.random() < 0.1:
                    draw.point((offset_x + x, y), fill=P[','])
        for _ in range(6):
            tx, ty = random.randint(2, 29), random.randint(2, 29)
            draw_grass_patch(offset_x + tx, ty)

    def fill_dirt(offset_x):
        # Irregular dirt path with soft sandy colors
        draw.rectangle([offset_x, 0, offset_x + 31, 31], fill=P['d'])
        for y in range(32):
            for x in range(32):
                r = random.random()
                if r < 0.15:
                    draw.point((offset_x + x, y), fill=P['D'])
                elif r < 0.25:
                    draw.point((offset_x + x, y), fill=P['l'])
        # Add a few small pebbles
        for _ in range(4):
            px, py = random.randint(2, 29), random.randint(2, 29)
            draw.point((offset_x + px, py), fill=P['r'])
            draw.point((offset_x + px, py+1), fill=P['D']) # pebble shadow

    random.seed(101) # new seed for new look

    # Tile 0: Base Grass
    fill_grass(0)

    # Tile 1: Flower Grass
    fill_grass(32)
    # Add clusters of JRPG-style small flowers
    for _ in range(5):
        fx = random.randint(3, 28)
        fy = random.randint(3, 28)
        color = P['w'] if random.random() > 0.4 else P['p']
        draw.point((32+fx-1, fy), fill=color)
        draw.point((32+fx+1, fy), fill=color)
        draw.point((32+fx, fy-1), fill=color)
        draw.point((32+fx, fy+1), fill=color)
        draw.point((32+fx, fy), fill=P['y'])

    # Tile 2: Dirt Path (Make it irregular, not a square crop)
    fill_dirt(64)
    # Add heavy organic grass edging around the dirt tile so it blends organically
    # instead of looking like a straight plowed field
    for y in range(32):
        for x in range(32):
            # Edges become grass
            dist_to_edge = min(x, 31-x, y, 31-y)
            if dist_to_edge < random.randint(2, 6):
                base = P['.'] if random.random() > 0.3 else P[',']
                draw.point((64+x, y), fill=base)
                if random.random() < 0.1:
                    draw.point((64+x, y), fill=P[';']) # shadow edge

    img.save(output_path)
    print(f"Generated JRPG Tileset at {output_path}")

def generate_arpg_tree(output_path):
    # Generates a Secret of Mana style bushy tree (64x64)
    width, height = 64, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Pixel Art Palette - Secret of Mana / Chrono Trigger vibes
    P = {
        'O': ( 24,  36,  24, 255), # Outline/Deep Shadow
        'T': ( 92,  64,  51, 255), # Trunk Base (Warm brown)
        't': ( 61,  43,  31, 255), # Trunk Shadow
        'c': ( 40,  28,  20, 255), # Trunk Deep Shadow / Bark lines
        '1': ( 28,  69,  40, 255), # Leaf Deep Shadow (Dark forest green)
        '2': ( 46, 105,  54, 255), # Leaf Shadow
        '3': ( 69, 145,  75, 255), # Leaf Base
        '4': (105, 186,  97, 255), # Leaf Highlight
        '5': (163, 219, 134, 255), # Leaf Extreme Highlight (Sunlight)
    }

    # ASCII Blueprint for an uneven, bushy JRPG tree (32x32 matrix, scale=2)
    tree_matrix = [
        "           OOOOOOOOO            ",
        "        OOO555544444OOO         ",
        "      OO555554444444433OO       ",
        "     O5555544443333444433O      ",
        "    O555444333333223344433O     ",
        "   O55443332221111222334433O    ",
        "  O54433222111OOOO1112233322O   ",
        "  O443322111OO3344OO11223322O   ",
        " O4432211OOO33445544O11223221O  ",
        " O433211O334455554433O1122211O  ",
        "O332211O44554433322211O1111111O ",
        "O32211O4455433221111OOO1111111O ",
        "O22111O334432211OOOO4433O11111O ",
        "O21111O2233211OO445554433O1111O ",
        " O1111O112211O33444332211O111O  ",
        " O1111OO1111O22332211111OO111O  ",
        "  O1111OOOOOO1122111OOOO1111O   ",
        "  OO11111111111111111111111OO   ",
        "    OOO11111111111111111OOO     ",
        "       OOOOOOO111OOOOOOO        ",
        "             OTTO               ",
        "            OtTTtO              ",
        "            OtccTO              ",
        "            OtTTcO              ",
        "           OotTTtcO             ",
        "          OotTcTccO             ",
        "          OotTccTtoO            ",
        "          OOOO  OOOO            ",
    ]

    draw_ascii_matrix(draw, tree_matrix, P, offset_x=0, offset_y=0, scale=2)

    # Add a soft drop shadow at the base
    draw.ellipse([20, 54, 44, 60], fill=(0, 0, 0, 100))

    img.save(output_path)
    print(f"Generated JRPG Tree at {output_path}")

def generate_arpg_player(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Classic JRPG hero palette (More detailed shading)
    P = {
        'O': ( 20,  20,  25, 255), # Deep Outline
        'S': (255, 219, 172, 255), # Skin Light
        's': (224, 172, 105, 255), # Skin Mid
        'd': (141,  85,  36, 255), # Skin Deep Shadow
        'H': (219,  65,   5, 255), # Hair Highlight (Bright Orange/Red)
        'h': (163,  35,   0, 255), # Hair Mid
        'i': ( 92,  15,   0, 255), # Hair Deep Shadow
        'B': ( 60, 100, 210, 255), # Shirt Blue Light
        'b': ( 35,  55, 140, 255), # Shirt Blue Shadow
        'C': ( 20,  30,  80, 255), # Shirt Deep Shadow
        'Y': (240, 190,  40, 255), # Trim/Belt Light
        'y': (160, 110,  15, 255), # Trim/Belt Shadow
        'P': ( 90,  90,  95, 255), # Pants
        'p': ( 55,  55,  60, 255), # Pants Shadow
        'L': ( 70,  40,  20, 255), # Leather Boots Light
        'l': ( 40,  20,  10, 255), # Leather Boots Shadow
        'e': (255, 255, 255, 255), # Eye whites
        'E': (  0,   0,   0, 255), # Eye pupils
    }

    # 16x24 Blueprint drawn at scale=1, centered
    # Better proportions: bigger hair volume, actual face details, defined arms and boots
    player_matrix = [
        "      OOOO      ",
        "     OHHHHO     ",
        "    OHhHHhHO    ",
        "   OhiHHhhiHO   ",
        "   OhSSSSSSHO   ",
        "   OHSeESeEHO   ",
        "   OhiSSSSiHO   ",
        "   OihsssshiO   ",
        "    OiiSSiiO    ",
        "     OOddOO     ",
        "     OYYYYO     ",
        "    OBBbbBBO    ",
        "   OSBbCCbBSO   ",
        "   OSbBBBBbSO   ",
        "   OsOBCbCOsO   ",
        "   OOOPPPPOOO   ",
        "      OPpO      ",
        "     OPppPO     ",
        "     OP  pO     ",
        "    OLLO OLLO   ",
        "    OlLO OlLO   ",
        "    OOOO OOOO   "
    ]

    # Center it: (32-16)/2 = 8, (32-22)/2 = 5
    draw_ascii_matrix(draw, player_matrix, P, offset_x=8, offset_y=5, scale=1)

    # Shadow underneath
    draw.ellipse([8, 28, 24, 31], fill=(0, 0, 0, 100))

    img.save(output_path)
    print(f"Generated JRPG Player at {output_path}")


if __name__ == "__main__":
    os.makedirs('assets/textures', exist_ok=True)
    generate_tileset('assets/textures/arpg_tileset.png')
    generate_arpg_tree('assets/textures/tree_arpg.png')
    generate_arpg_player('assets/textures/player_arpg.png')
