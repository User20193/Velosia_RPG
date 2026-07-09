from PIL import Image
img = Image.open('src_image.png')
print(f"Format: {img.format}, Mode: {img.mode}, Size: {img.size}")
has_alpha = False
if img.mode == 'RGBA':
    for pixel in img.getdata():
        if pixel[3] < 255:
            has_alpha = True
            break
print(f"Has transparent pixels: {has_alpha}")
