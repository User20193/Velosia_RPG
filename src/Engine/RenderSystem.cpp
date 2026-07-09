#include "RenderSystem.hpp"
#include "Components.hpp"
#include "DisplayManager.hpp"
#include <raylib.h>
#include <algorithm>

namespace Velosia::Engine {

    static RenderTexture2D targetCanvas;

    void RenderSystem::InitWindow(int width, int height, const std::string& title) {
        SetConfigFlags(FLAG_WINDOW_RESIZABLE);
        ::InitWindow(width, height, title.c_str());

        DisplayManager::SetInternalResolution(width, height);
        targetCanvas = LoadRenderTexture(width, height);
        SetTextureFilter(targetCanvas.texture, TEXTURE_FILTER_POINT);

        SetTargetFPS(60);
    }

    void RenderSystem::CloseWindow() {
        UnloadRenderTexture(targetCanvas);
        ::CloseWindow();
    }

    bool RenderSystem::ShouldClose() { return WindowShouldClose(); }

    void RenderSystem::BeginDraw() {
        if (targetCanvas.texture.width != DisplayManager::GetInternalWidth() ||
            targetCanvas.texture.height != DisplayManager::GetInternalHeight()) {
            UnloadRenderTexture(targetCanvas);
            targetCanvas = LoadRenderTexture(DisplayManager::GetInternalWidth(), DisplayManager::GetInternalHeight());
            SetTextureFilter(targetCanvas.texture, TEXTURE_FILTER_POINT);
        }

        BeginTextureMode(targetCanvas);
        ClearBackground(RAYWHITE);
    }

    void RenderSystem::EndDraw() {
        EndTextureMode();

        BeginDrawing();
        ClearBackground(BLACK);

        float scale = std::min(
            (float)GetScreenWidth() / DisplayManager::GetInternalWidth(),
            (float)GetScreenHeight() / DisplayManager::GetInternalHeight()
        );

        Rectangle sourceRec = { 0.0f, 0.0f, (float)targetCanvas.texture.width, (float)-targetCanvas.texture.height };
        Rectangle destRec = {
            (GetScreenWidth() - ((float)DisplayManager::GetInternalWidth() * scale)) * 0.5f,
            (GetScreenHeight() - ((float)DisplayManager::GetInternalHeight() * scale)) * 0.5f,
            (float)DisplayManager::GetInternalWidth() * scale,
            (float)DisplayManager::GetInternalHeight() * scale
        };

        DrawTexturePro(targetCanvas.texture, sourceRec, destRec, {0, 0}, 0.0f, WHITE);
        EndDrawing();
    }

    void RenderSystem::TakeScreenshot(const std::string& filename) {
        ::TakeScreenshot(filename.c_str());
    }

    void RenderSystem::DrawEntities(ECSManager& ecs) {
        auto view = ecs.GetRegistry().view<TransformComponent>();
        for (auto entity : view) {
            auto& transform = view.get<TransformComponent>(entity);
            // Draw a simple 32x32 colored square as a placeholder
            DrawRectangle(static_cast<int>(transform.x), static_cast<int>(transform.y), 32, 32, RED);
        }
    }
}
