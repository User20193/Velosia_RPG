#pragma once
#include <entt.hpp>
namespace Velosia::Engine {
    class ECSManager {
    public:
        ECSManager() = default;
        entt::entity CreateEntity() { return registry.create(); }
        void DestroyEntity(entt::entity entity) { registry.destroy(entity); }
        entt::registry& GetRegistry() { return registry; }
        void Clear() { registry.clear(); }
    private:
        entt::registry registry;
    };
}
