#pragma once
#include "ECSManager.hpp"
#include <string>

namespace Velosia::Engine {

    class PlayerInputSystem {
    public:
        // Reads Input and applies velocity only to entities with a specific Tag (e.g. "Player")
        static void Update(ECSManager& ecs, const std::string& playerTag, float speed);
    };

}
