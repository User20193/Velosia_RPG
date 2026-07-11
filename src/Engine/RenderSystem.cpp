#include "RenderSystem.hpp"
#include "Components.hpp"
#include "DisplayManager.hpp"
#include "ResourceManager.hpp"
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
        // User requested removing the "white void". Changing to BLACK.
        ClearBackground(BLACK);
    }

    void RenderSystem::EndDraw() {
        EndTextureMode();

        BeginDrawing();
        ClearBackground(BLACK);

        int internalWidth = DisplayManager::GetInternalWidth();
        int internalHeight = DisplayManager::GetInternalHeight();

        if (internalWidth <= 0 || internalHeight <= 0) {
            EndDrawing();
            return;
        }

        float scale = std::min(
            (float)GetScreenWidth() / internalWidth,
            (float)GetScreenHeight() / internalHeight
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

    void RenderSystem::DrawTexture(const std::string& textureId, float x, float y, float scale, unsigned char r, unsigned char g, unsigned char b, unsigned char a) {
        Texture2D* tex = ResourceManager::GetInstance().GetTexture(textureId);
        if (tex != nullptr) {
            Color tint = { r, g, b, a };
            DrawTextureEx(*tex, {x, y}, 0.0f, scale, tint);
        } else {
             // Silently fail if texture missing for UI flexibility or we can log it if needed
        }
    }

    void RenderSystem::DrawText(const std::string& fontId, const std::string& text, float x, float y, float fontSize, float spacing, unsigned char r, unsigned char g, unsigned char b, unsigned char a) {
        Font* font = ResourceManager::GetInstance().GetFont(fontId);
        Color tint = { r, g, b, a };
        if (font != nullptr) {
            DrawTextEx(*font, text.c_str(), {x, y}, fontSize, spacing, tint);
        } else {
            // Fallback to default raylib font
            ::DrawText(text.c_str(), static_cast<int>(x), static_cast<int>(y), static_cast<int>(fontSize), tint);
        }
    }

    float RenderSystem::MeasureTextWidth(const std::string& fontId, const std::string& text, float fontSize, float spacing) {
        Font* font = ResourceManager::GetInstance().GetFont(fontId);
        if (font != nullptr) {
            Vector2 size = MeasureTextEx(*font, text.c_str(), fontSize, spacing);
            return size.x;
        }
        return static_cast<float>(MeasureText(text.c_str(), static_cast<int>(fontSize)));
    }

    void RenderSystem::DrawEntities(ECSManager& ecs) {
        // Fallback: draw red rectangle if only transform exists
        auto viewRect = ecs.GetRegistry().view<TransformComponent>(entt::exclude<SpriteComponent>);
        for (auto entity : viewRect) {
            auto& transform = viewRect.get<TransformComponent>(entity);
            DrawRectangle(static_cast<int>(transform.x), static_cast<int>(transform.y), 32, 32, RED);
        }

        // Draw proper sprites if SpriteComponent exists
        auto viewSprite = ecs.GetRegistry().view<TransformComponent, SpriteComponent>();
        for (auto entity : viewSprite) {
            auto& transform = viewSprite.get<TransformComponent>(entity);
            auto& sprite = viewSprite.get<SpriteComponent>(entity);

            Texture2D* tex = ResourceManager::GetInstance().GetTexture(sprite.textureId);
            if (tex != nullptr) {
                Rectangle sourceRec = {
                    (float)sprite.srcX, (float)sprite.srcY,
                    (float)sprite.srcWidth, (float)sprite.srcHeight
                };
                Rectangle destRec = {
                    transform.x, transform.y,
                    sprite.srcWidth * sprite.scale, sprite.srcHeight * sprite.scale
                };
                Vector2 origin = { 0.0f, 0.0f }; // Top-left origin
                Color tint = { sprite.tintR, sprite.tintG, sprite.tintB, sprite.tintA };

                DrawTexturePro(*tex, sourceRec, destRec, origin, 0.0f, tint);
            } else {
                // Fallback to magenta rectangle if texture missing
                DrawRectangle(static_cast<int>(transform.x), static_cast<int>(transform.y), sprite.srcWidth, sprite.srcHeight, MAGENTA);
            }
        }
    }
}
