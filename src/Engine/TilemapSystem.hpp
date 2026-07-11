#pragma once

#include <vector>
#include <string>

namespace Velosia::Engine {

    class TilemapSystem {
    public:
        // Renders a grid of integers using a loaded texture atlas
        // mapData is a 1D array representing a 2D grid
        // mapWidth, mapHeight are in tiles
        // tileSize is the pixel size of each tile (e.g., 32x32)
        // textureId is the string ID of the tileset in the ResourceManager
        // columnsInTileset represents how many tiles wide the source texture is
        static void DrawMap(const std::vector<int>& mapData, int mapWidth, int mapHeight, int tileSize, const std::string& textureId, int columnsInTileset);
    };

}
