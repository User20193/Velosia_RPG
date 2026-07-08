#include <pybind11/pybind11.h>
#include "Logger.hpp"
#include "PAL.hpp"
#include "Memory.hpp"
#include "ECSManager.hpp"
#include "Components.hpp"
#include "RenderSystem.hpp"

namespace py = pybind11;

PYBIND11_MODULE(velosia_core, m) {
    m.doc() = "Velosia Engine Core Module";

    m.def("init", []() {
        Velosia::Core::Logger::Init();
        Velosia::Core::Memory::Init();
        Velosia::Core::PAL::Init();
    });

    m.def("shutdown", []() {
        Velosia::Core::PAL::Shutdown();
        Velosia::Core::Memory::Shutdown();
    });

    py::class_<Velosia::Core::Logger>(m, "Logger")
        .def_static("info", &Velosia::Core::Logger::Info)
        .def_static("warn", &Velosia::Core::Logger::Warn)
        .def_static("error", &Velosia::Core::Logger::Error)
        .def_static("fatal", &Velosia::Core::Logger::Fatal);

    py::class_<Velosia::Engine::TransformComponent>(m, "TransformComponent")
        .def(py::init<>())
        .def_readwrite("x", &Velosia::Engine::TransformComponent::x)
        .def_readwrite("y", &Velosia::Engine::TransformComponent::y);

    py::class_<Velosia::Engine::VelocityComponent>(m, "VelocityComponent")
        .def(py::init<>())
        .def_readwrite("dx", &Velosia::Engine::VelocityComponent::dx)
        .def_readwrite("dy", &Velosia::Engine::VelocityComponent::dy);

    py::class_<Velosia::Engine::TagComponent>(m, "TagComponent")
        .def(py::init<>())
        .def_readwrite("tag", &Velosia::Engine::TagComponent::tag);

    py::class_<Velosia::Engine::RenderSystem>(m, "RenderSystem")
        .def_static("init_window", &Velosia::Engine::RenderSystem::InitWindow)
        .def_static("close_window", &Velosia::Engine::RenderSystem::CloseWindow)
        .def_static("should_close", &Velosia::Engine::RenderSystem::ShouldClose)
        .def_static("begin_draw", &Velosia::Engine::RenderSystem::BeginDraw)
        .def_static("end_draw", &Velosia::Engine::RenderSystem::EndDraw)
        .def_static("draw_entities", &Velosia::Engine::RenderSystem::DrawEntities);

    py::class_<Velosia::Engine::ECSManager>(m, "ECSManager")
        .def(py::init<>())
        .def("create_entity", [](Velosia::Engine::ECSManager& self) { return static_cast<uint32_t>(self.CreateEntity()); })
        .def("destroy_entity", [](Velosia::Engine::ECSManager& self, uint32_t entity) { self.DestroyEntity(static_cast<entt::entity>(entity)); })
        .def("clear", &Velosia::Engine::ECSManager::Clear)
        .def("add_transform", [](Velosia::Engine::ECSManager& self, uint32_t entity, float x, float y) {
            auto& comp = self.GetRegistry().emplace<Velosia::Engine::TransformComponent>(static_cast<entt::entity>(entity));
            comp.x = x; comp.y = y;
        })
        .def("get_transform", [](Velosia::Engine::ECSManager& self, uint32_t entity) {
            return &self.GetRegistry().get<Velosia::Engine::TransformComponent>(static_cast<entt::entity>(entity));
        }, py::return_value_policy::reference)
        .def("add_velocity", [](Velosia::Engine::ECSManager& self, uint32_t entity, float dx, float dy) {
            auto& comp = self.GetRegistry().emplace<Velosia::Engine::VelocityComponent>(static_cast<entt::entity>(entity));
            comp.dx = dx; comp.dy = dy;
        })
        .def("get_velocity", [](Velosia::Engine::ECSManager& self, uint32_t entity) {
            return &self.GetRegistry().get<Velosia::Engine::VelocityComponent>(static_cast<entt::entity>(entity));
        }, py::return_value_policy::reference)
        .def("add_tag", [](Velosia::Engine::ECSManager& self, uint32_t entity, const std::string& tag) {
            auto& comp = self.GetRegistry().emplace<Velosia::Engine::TagComponent>(static_cast<entt::entity>(entity));
            comp.tag = tag;
        })
        .def("get_tag", [](Velosia::Engine::ECSManager& self, uint32_t entity) {
            return &self.GetRegistry().get<Velosia::Engine::TagComponent>(static_cast<entt::entity>(entity));
        }, py::return_value_policy::reference);
}
