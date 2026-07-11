#include "PlayerInputSystem.hpp"
#include "Components.hpp"
#include "Input.hpp"

namespace Velosia::Engine {

    void PlayerInputSystem::Update(ECSManager& ecs, const std::string& playerTag, float speed) {
        auto view = ecs.GetRegistry().view<TagComponent, VelocityComponent>();

        for (auto entity : view) {
            auto& tag = view.get<TagComponent>(entity);

            if (tag.tag == playerTag) {
                auto& velocity = view.get<VelocityComponent>(entity);

                float input_dx = 0.0f;
                float input_dy = 0.0f;

                if (Input::IsKeyDown(Input::Key::W) || Input::IsKeyDown(Input::Key::UP)) input_dy -= speed;
                if (Input::IsKeyDown(Input::Key::S) || Input::IsKeyDown(Input::Key::DOWN)) input_dy += speed;
                if (Input::IsKeyDown(Input::Key::A) || Input::IsKeyDown(Input::Key::LEFT)) input_dx -= speed;
                if (Input::IsKeyDown(Input::Key::D) || Input::IsKeyDown(Input::Key::RIGHT)) input_dx += speed;

                // Normalize diagonal movement speed
                if (input_dx != 0.0f && input_dy != 0.0f) {
                    input_dx *= 0.7071f;
                    input_dy *= 0.7071f;
                }

                // Only overwrite if the player is actively moving, allowing MovementSystem bouncing to persist
                if (input_dx != 0.0f || input_dy != 0.0f) {
                    velocity.dx = input_dx;
                    velocity.dy = input_dy;
                } else {
                     // Decelerate naturally instead of forced 0 (simple friction)
                     velocity.dx *= 0.8f;
                     velocity.dy *= 0.8f;
                }
            }
        }
    }
}
