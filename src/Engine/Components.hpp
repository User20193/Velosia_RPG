#pragma once
#include <string>
namespace Velosia::Engine {
    struct TransformComponent { float x = 0.0f; float y = 0.0f; };
    struct VelocityComponent { float dx = 0.0f; float dy = 0.0f; };
    struct TagComponent { std::string tag; };
}
