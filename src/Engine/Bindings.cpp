#include <pybind11/pybind11.h>
#include "Logger.hpp"
#include "PAL.hpp"
#include "Memory.hpp"
#include "ECSManager.hpp"
#include "Components.hpp"
#include "RenderSystem.hpp"
#include "MovementSystem.hpp"
#include "EventBus.hpp"
#include "Input.hpp"
#include "PlayerInputSystem.hpp"
#include "DisplayManager.hpp"
#include <pybind11/functional.h> // Needed for passing Python functions to std::function

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
        .def_static("take_screenshot", &Velosia::Engine::RenderSystem::TakeScreenshot, py::arg("filename"))
        .def_static("draw_entities", &Velosia::Engine::RenderSystem::DrawEntities);

    py::class_<Velosia::Engine::MovementSystem>(m, "MovementSystem")
        .def_static("update", &Velosia::Engine::MovementSystem::Update);

    // Event Bus
    py::class_<Velosia::Engine::EventBus>(m, "EventBus")
        .def_static("get_instance", &Velosia::Engine::EventBus::GetInstance, py::return_value_policy::reference)
        .def("subscribe", &Velosia::Engine::EventBus::Subscribe)
        .def("emit", &Velosia::Engine::EventBus::Emit, py::arg("event_type"), py::arg("payload") = "")
        .def("clear", &Velosia::Engine::EventBus::Clear);

    // Input System
    py::enum_<Velosia::Engine::Input::Key>(m, "Key")
        .value("W", Velosia::Engine::Input::Key::W)
        .value("A", Velosia::Engine::Input::Key::A)
        .value("S", Velosia::Engine::Input::Key::S)
        .value("D", Velosia::Engine::Input::Key::D)
        .value("UP", Velosia::Engine::Input::Key::UP)
        .value("DOWN", Velosia::Engine::Input::Key::DOWN)
        .value("LEFT", Velosia::Engine::Input::Key::LEFT)
        .value("RIGHT", Velosia::Engine::Input::Key::RIGHT)
        .value("SPACE", Velosia::Engine::Input::Key::SPACE)
        .value("ENTER", Velosia::Engine::Input::Key::ENTER)
        .value("ESCAPE", Velosia::Engine::Input::Key::ESCAPE)
        .export_values();

    py::class_<Velosia::Engine::Input>(m, "Input")
        .def_static("is_key_pressed", &Velosia::Engine::Input::IsKeyPressed)
        .def_static("is_key_down", &Velosia::Engine::Input::IsKeyDown)
        .def_static("is_key_released", &Velosia::Engine::Input::IsKeyReleased)
        .def_static("is_key_up", &Velosia::Engine::Input::IsKeyUp);

    py::class_<Velosia::Engine::PlayerInputSystem>(m, "PlayerInputSystem")
        .def_static("update", &Velosia::Engine::PlayerInputSystem::Update, py::arg("ecs"), py::arg("player_tag"), py::arg("speed"));

    py::class_<Velosia::Engine::DisplayManager>(m, "DisplayManager")
        .def_static("set_internal_resolution", &Velosia::Engine::DisplayManager::SetInternalResolution)
        .def_static("set_window_size", &Velosia::Engine::DisplayManager::SetWindowSize)
        .def_static("toggle_fullscreen", &Velosia::Engine::DisplayManager::ToggleFullscreen)
        .def_static("set_borderless", &Velosia::Engine::DisplayManager::SetBorderless)
        .def_static("get_internal_width", &Velosia::Engine::DisplayManager::GetInternalWidth)
        .def_static("get_internal_height", &Velosia::Engine::DisplayManager::GetInternalHeight)
        .def_static("get_window_width", &Velosia::Engine::DisplayManager::GetWindowWidth)
        .def_static("get_window_height", &Velosia::Engine::DisplayManager::GetWindowHeight);

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
