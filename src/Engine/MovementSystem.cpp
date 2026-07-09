#include "MovementSystem.hpp"
#include "Components.hpp"

namespace Velosia::Engine {

    void MovementSystem::Update(ECSManager& ecs) {
        // EnTT's view is incredibly fast due to cache locality
        auto view = ecs.GetRegistry().view<TransformComponent, VelocityComponent>();

        for (auto entity : view) {
            auto& transform = view.get<TransformComponent>(entity);
            auto& velocity = view.get<VelocityComponent>(entity);

            transform.x += velocity.dx;
            transform.y += velocity.dy;

            // Basic bounding box bounce logic inside C++
            // Accounts for 32px entity bounds!
            if (transform.x > 800 - 32 || transform.x < 0) velocity.dx *= -1;
            if (transform.y > 600 - 32 || transform.y < 0) velocity.dy *= -1;

            // Prevent getting stuck outside bounds
            if (transform.x < 0) transform.x = 0;
            if (transform.y < 0) transform.y = 0;
            if (transform.x > 800 - 32) transform.x = 800 - 32;
            if (transform.y > 600 - 32) transform.y = 600 - 32;
        }
    }

}
