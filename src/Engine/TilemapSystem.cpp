#include "TilemapSystem.hpp"
#include "ResourceManager.hpp"
#include "../Core/Logger.hpp"
#include <raylib.h>

namespace Velosia::Engine {

    void TilemapSystem::DrawMap(const std::vector<int>& mapData, int mapWidth, int mapHeight, int tileSize, const std::string& textureId, int columnsInTileset) {
        Texture2D* tex = ResourceManager::GetInstance().GetTexture(textureId);

        if (tex == nullptr) {
            // Silently fail or log sparingly (to avoid flooding console every frame)
            return;
        }

        if (columnsInTileset <= 0) return;

        if (mapData.size() < (size_t)(mapWidth * mapHeight)) {
            Velosia::Core::Logger::Error("TilemapSystem: mapData size is smaller than mapWidth * mapHeight.");
            return;
        }

        for (int y = 0; y < mapHeight; ++y) {
            for (int x = 0; x < mapWidth; ++x) {
                int tileIndex = mapData[y * mapWidth + x];

                // Usually 0 or -1 implies empty space (no tile)
                if (tileIndex <= 0) continue;

                // Convert 1-based or 0-based index to 2D coordinates on the spritesheet
                // Assuming 1-based index (0 is empty)
                int actualIndex = tileIndex - 1;
                int srcX = (actualIndex % columnsInTileset) * tileSize;
                int srcY = (actualIndex / columnsInTileset) * tileSize;

                Rectangle sourceRec = { (float)srcX, (float)srcY, (float)tileSize, (float)tileSize };
                Vector2 position = { (float)(x * tileSize), (float)(y * tileSize) };

                DrawTextureRec(*tex, sourceRec, position, WHITE);
            }
        }
    }

}
