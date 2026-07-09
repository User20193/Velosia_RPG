from PIL import Image

img = Image.open('original.png').convert('RGBA')
width, height = img.size
pixels = img.load()

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # is grayscale?
        if max(abs(r-g), abs(r-b), abs(g-b)) < 15:
            # is light or dark checkerboard?
            if (230 <= r <= 255) or (190 <= r <= 210):
                pixels[x, y] = (r, g, b, 0)

img.save('test_removed.png')
