from PIL import Image
img = Image.open('assets/sprites/tilesets/grass.png').convert('RGBA')
resized = img.resize((32, 32), Image.Resampling.NEAREST)
resized.save('assets/sprites/tilesets/grass_tile.png')
print("Extracted 32x32 grass tile")
