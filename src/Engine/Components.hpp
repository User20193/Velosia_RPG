#pragma once
#include <string>
namespace Velosia::Engine {
    struct TransformComponent { float x = 0.0f; float y = 0.0f; };
    struct VelocityComponent { float dx = 0.0f; float dy = 0.0f; };
    struct TagComponent { std::string tag; };

    struct SpriteComponent {
        std::string textureId;
        float scale = 1.0f;
        int srcX = 0; // For spritesheet animation logic later
        int srcY = 0;
        int srcWidth = 32;
        int srcHeight = 32;
        unsigned char tintR = 255;
        unsigned char tintG = 255;
        unsigned char tintB = 255;
        unsigned char tintA = 255;
        float rotation = 0.0f;
        float originX = 0.0f;
        float originY = 0.0f;
    };
}
