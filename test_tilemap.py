import sys
import os
sys.path.append('build')
import velosia_core

print("Initializing Display")
velosia_core.RenderSystem.init_window(800, 600, "Tilemap Test")

print("Loading Texture")
velosia_core.ResourceManager.get_instance().load_texture("grass_tileset", "assets/sprites/tilesets/grass_tile.png")

print("Generating Map")
map_data = [1] * (25 * 20)

for _ in range(2):
    velosia_core.RenderSystem.begin_draw()
    velosia_core.TilemapSystem.draw_map(map_data, 25, 20, 32, "grass_tileset", 1)
    velosia_core.RenderSystem.end_draw()

print("Clearing textures")
velosia_core.ResourceManager.get_instance().clear_textures()
print("Success")
velosia_core.RenderSystem.close_window()
