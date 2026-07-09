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

        # Turn white into transparent, but more aggressively to remove halos
        # Let's just find the bounding box of non-white pixels, and then scale the whole layer
        # wait, we shouldn't crop to bbox and then scale. The layer itself contains transparent space to place the objects correctly on the screen!
        # So we should just remove the white background, and scale the *entire layer* to 1366x768 (or maintain aspect ratio relative to 768)

        # Make white transparent
        datas = layer.getdata()
        newData = []
        for item in datas:
            # More aggressive threshold to catch anti-aliased edges, or just exact white if it's pure pixel art
            # Let's say anything > 200 is white background.
            if item[0] >= 200 and item[1] >= 200 and item[2] >= 200:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        layer.putdata(newData)

        out_path = os.path.join(output_dir, f"bg_layer{i+1}.png")

        # We need to scale the *entire layer box* so that layer objects remain in their correct relative positions.
        target_height = 768
        ratio = target_height / layer.height
        target_width = int(layer.width * ratio)

        # Use NEAREST to preserve pixel art look
        resized_layer = layer.resize((target_width, target_height), Image.Resampling.NEAREST)

        resized_layer.save(out_path)
        print(f"Saved layer {i+1} to {out_path} (Size: {target_width}x{target_height})")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 image_slicer.py <input_image> <output_dir>")
        sys.exit(1)
    slice_image(sys.argv[1], sys.argv[2])
