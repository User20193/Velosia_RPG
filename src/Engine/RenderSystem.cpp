#include "RenderSystem.hpp"
#include "Components.hpp"
#include <raylib.h>

namespace Velosia::Engine {
    void RenderSystem::InitWindow(int width, int height, const std::string& title) {
        ::InitWindow(width, height, title.c_str());
        SetTargetFPS(60);
    }
    void RenderSystem::CloseWindow() { ::CloseWindow(); }
    bool RenderSystem::ShouldClose() { return WindowShouldClose(); }
    void RenderSystem::BeginDraw() {
        BeginDrawing();
        ClearBackground(RAYWHITE);
    }
    void RenderSystem::EndDraw() { EndDrawing(); }

    void RenderSystem::DrawEntities(ECSManager& ecs) {
        auto view = ecs.GetRegistry().view<TransformComponent>();
        for (auto entity : view) {
            auto& transform = view.get<TransformComponent>(entity);
            // Draw a simple 32x32 colored square as a placeholder
            DrawRectangle(static_cast<int>(transform.x), static_cast<int>(transform.y), 32, 32, RED);
        }
    }
}
