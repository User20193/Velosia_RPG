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

    # Palette
    P = {
        '.': (116, 186, 104, 255), # Grass Light
        ',': (89,  158,  78, 255), # Grass Mid
        ';': (55,  110,  46, 255), # Grass Dark
        'w': (240, 240, 240, 255), # White Flower
        'y': (245, 215,  66, 255), # Yellow Flower Center
        'd': (184, 138,  92, 255), # Dirt Base
        'D': (150, 105,  65, 255), # Dirt Shadow
        'l': (209, 172, 134, 255), # Dirt Highlight
    }

    # Helper to fill random base with noise
    def fill_grass(offset_x):
        for y in range(32):
            for x in range(32):
                r = random.random()
                c = '.' if r > 0.3 else (',' if r > 0.05 else ';')
                draw.point((offset_x + x, y), fill=P[c])

    def fill_dirt(offset_x):
        for y in range(32):
            for x in range(32):
                r = random.random()
                c = 'd' if r > 0.2 else ('D' if r > 0.05 else 'l')
                draw.point((offset_x + x, y), fill=P[c])

    random.seed(42)
    # Tile 0: Base Grass
    fill_grass(0)

    # Tile 1: Flower Grass
    fill_grass(32)
    # Add a few small pixel flowers
    for _ in range(4):
        fx = random.randint(2, 28)
        fy = random.randint(2, 28)
        draw.point((32+fx-1, fy), fill=P['w'])
        draw.point((32+fx+1, fy), fill=P['w'])
        draw.point((32+fx, fy-1), fill=P['w'])
        draw.point((32+fx, fy+1), fill=P['w'])
        draw.point((32+fx, fy), fill=P['y'])

    # Tile 2: Dirt Path
    fill_dirt(64)
    # Add grass edging to dirt
    for y in range(32):
        for x in range(32):
            if x < 4 or x > 27 or y < 4 or y > 27:
                if random.random() > 0.4:
                     draw.point((64+x, y), fill=P[';'])

    img.save(output_path)
    print(f"Generated Tileset at {output_path}")

def generate_arpg_tree(output_path):
    # Generates a Secret of Mana style round tree (64x64)
    width, height = 64, 64
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Pixel Art Palette
    P = {
        'O': ( 24,  36,  24, 255), # Outline
        'T': (105,  66,  36, 255), # Trunk Base
        't': ( 71,  40,  18, 255), # Trunk Shadow
        '1': ( 36,  92,  36, 255), # Leaf Deep Shadow
        '2': ( 55, 148,  55, 255), # Leaf Mid
        '3': ( 92, 194,  92, 255), # Leaf Light
        '4': (144, 224, 144, 255), # Leaf Highlight
    }

    # ASCII Blueprint for top half of tree (scaled x2 for chunkiness)
    # 32x32 matrix, drawn at scale=2 to fill 64x64
    tree_matrix = [
        "           OOOOOOOOO            ",
        "        OOO333333333OOO         ",
        "      OO333333444433333OO       ",
        "     O3333344444444333333O      ",
        "    O333344444444444333333O     ",
        "   O33344444444444444333333O    ",
        "  O3334444444444444444333333O   ",
        "  O3333444444444444443333333O   ",
        " O333333444444444444333333333O  ",
        " O233333334444444433333333332O  ",
        "O12233333333333333333333333221O ",
        "O11222333333333333333333322211O ",
        "O11122223333333333333332222111O ",
        "O11112222233333333332222211111O ",
        " O111112222222222222222111111O  ",
        " O111111122222222222211111111O  ",
        "  O1111111111111111111111111O   ",
        "  OO11111111111111111111111OO   ",
        "    OOO11111111111111111OOO     ",
        "       OOOOOOO111OOOOOOO        ",
        "             OTTO               ",
        "             OTtO               ",
        "             OTtO               ",
        "             OTtO               ",
        "            OOTtOO              ",
        "           OTTTttO              ",
        "           OTtOOtO              ",
        "           OOO  OO              ",
    ]

    draw_ascii_matrix(draw, tree_matrix, P, offset_x=0, offset_y=0, scale=2)
    img.save(output_path)
    print(f"Generated ARPG Tree at {output_path}")

def generate_arpg_player(output_path):
    width, height = 32, 32
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Secret of Mana / Stardew Valley proportioned character
    P = {
        'O': (  0,   0,   0, 255), # Outline
        'S': (255, 213, 170, 255), # Skin
        's': (220, 163, 110, 255), # Skin Shadow
        'H': (212,  88,  34, 255), # Hair (Red/Orange hero hair)
        'h': (140,  45,  10, 255), # Hair shadow
        'B': ( 40,  80, 200, 255), # Shirt Blue
        'b': ( 20,  40, 120, 255), # Shirt Shadow
        'Y': (230, 200,  30, 255), # Scarf/Trim Yellow
        'P': (100, 100, 100, 255), # Pants
        'L': ( 60,  30,  10, 255), # Leather Boots
    }

    # 16x24 Blueprint drawn at scale=1, centered
    player_matrix = [
        "      OOOO      ",
        "     OHHHHO     ",
        "    OHHHHHHO    ",
        "    OHhHHhHO    ",
        "   OHHSSSSHO    ",
        "   OHOSOSOHO    ",
        "   OHSSSSSHO    ",
        "   OHHsssHHO    ",
        "    OHHHHHHO    ",
        "     OOOOOO     ",
        "     OYYYYO     ",
        "    OBBBBbBO    ",
        "   OBBBBBbbBO   ",
        "   OBbBBbBbBO   ",
        "   OSOBBBBOSO   ",
        "   OSOBbBbOSO   ",
        "   OOOPPPPOOO   ",
        "      OPPO      ",
        "     OPPPPO     ",
        "     OP  PO     ",
        "    OLLO OLLO   ",
        "    OLLO OLLO   ",
        "    OOOO OOOO   "
    ]

    # Center it: (32-16)/2 = 8, (32-24)/2 = 4
    draw_ascii_matrix(draw, player_matrix, P, offset_x=8, offset_y=4, scale=1)

    # Shadow underneath
    draw.ellipse([8, 28, 24, 31], fill=(0, 0, 0, 100))

    img.save(output_path)
    print(f"Generated ARPG Player at {output_path}")


if __name__ == "__main__":
    os.makedirs('assets/textures', exist_ok=True)
    generate_tileset('assets/textures/arpg_tileset.png')
    generate_arpg_tree('assets/textures/tree_arpg.png')
    generate_arpg_player('assets/textures/player_arpg.png')
