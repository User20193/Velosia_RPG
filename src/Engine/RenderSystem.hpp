#pragma once
#include "ECSManager.hpp"
#include <string>

namespace Velosia::Engine {
    class RenderSystem {
    public:
        static void InitWindow(int width, int height, const std::string& title);
        static void CloseWindow();
        static bool ShouldClose();

        static void BeginDraw(); // Begins drawing to the internal canvas
        static void EndDraw();   // Finishes internal drawing, scales, and draws to the external window

        static void TakeScreenshot(const std::string& filename);

        // Draws a texture directly (useful for UI/Backgrounds outside of ECS)
        static void DrawTexture(const std::string& textureId, float x, float y, float scale, unsigned char r, unsigned char g, unsigned char b, unsigned char a);

        // Draws Text using a loaded custom font
        static void DrawText(const std::string& fontId, const std::string& text, float x, float y, float fontSize, float spacing, unsigned char r, unsigned char g, unsigned char b, unsigned char a);

        // The ECS System: loops through all entities with Transform and draws them
        static void DrawEntities(ECSManager& ecs);
    };
}
