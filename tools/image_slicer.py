import sys
import os
from PIL import Image

def slice_image(input_path, output_dir):
    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Failed to open image: {e}")
        return

    width, height = img.size
    print(f"Original image size: {width}x{height}")

    num_layers = 6
    layer_height = height // num_layers

    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_layers):
        top = i * layer_height
        bottom = (i + 1) * layer_height
        box = (0, top, width, bottom)
        layer = img.crop(box)

        # Remove the checkerboard background
        pixels = layer.load()
        for y in range(layer.height):
            for x in range(layer.width):
                r, g, b, a = pixels[x, y]
                # is grayscale?
                if max(abs(r-g), abs(r-b), abs(g-b)) < 20:
                    # is light or dark checkerboard?
                    if (225 <= r <= 255) or (185 <= r <= 215):
                        pixels[x, y] = (r, g, b, 0)

        out_path = os.path.join(output_dir, f"bg_layer{i+1}.png")

        # The user's original image was 926x1197. Each layer is 926x199.
        # We need to scale to fit 768 height.
        # So layer height goes from 199 to 768.
        # We need to preserve aspect ratio.
        target_height = 768
        ratio = target_height / layer.height
        target_width = int(layer.width * ratio)

        resized_layer = layer.resize((target_width, target_height), Image.Resampling.NEAREST)
        resized_layer.save(out_path)
        print(f"Saved layer {i+1} to {out_path} (Size: {target_width}x{target_height})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 image_slicer.py <input_image> <output_dir>")
        sys.exit(1)
    slice_image(sys.argv[1], sys.argv[2])
