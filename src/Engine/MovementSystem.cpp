#include "MovementSystem.hpp"
#include "Components.hpp"
#include "DisplayManager.hpp"

namespace Velosia::Engine {

    void MovementSystem::Update(ECSManager& ecs) {
        // EnTT's view is incredibly fast due to cache locality
        auto view = ecs.GetRegistry().view<TransformComponent, VelocityComponent>();

        int screenWidth = DisplayManager::GetInternalWidth();
        int screenHeight = DisplayManager::GetInternalHeight();

        for (auto entity : view) {
            auto& transform = view.get<TransformComponent>(entity);
            auto& velocity = view.get<VelocityComponent>(entity);

            transform.x += velocity.dx;
            transform.y += velocity.dy;

            // Basic bounding box bounce logic inside C++
            // Accounts for 32px entity bounds!
            if (transform.x > screenWidth - 32 || transform.x < 0) velocity.dx *= -1;
            if (transform.y > screenHeight - 32 || transform.y < 0) velocity.dy *= -1;

            // Prevent getting stuck outside bounds
            if (transform.x < 0) transform.x = 0;
            if (transform.y < 0) transform.y = 0;
            if (transform.x > screenWidth - 32) transform.x = screenWidth - 32;
            if (transform.y > screenHeight - 32) transform.y = screenHeight - 32;
        }
    }

}
