#pragma once
#include "ECSManager.hpp"

namespace Velosia::Engine {

    class MovementSystem {
    public:
        // Update all entities that have both Transform and Velocity
        static void Update(ECSManager& ecs);
    };

}
