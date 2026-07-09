#pragma once
#include "ECSManager.hpp"
#include <string>

namespace Velosia::Engine {
    class RenderSystem {
    public:
        static void InitWindow(int width, int height, const std::string& title);
        static void CloseWindow();
        static bool ShouldClose();

        static void BeginDraw();
        static void EndDraw();

        static void TakeScreenshot(const std::string& filename);

        // The ECS System: loops through all entities with Transform and draws them
        static void DrawEntities(ECSManager& ecs);
    };
}
