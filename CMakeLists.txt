cmake_minimum_required(VERSION 3.15)
project(VelosiaEngine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build as a shared library for Python
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find Python and Pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
add_subdirectory(third_party/pybind11)

# EnTT (Header only)
add_library(entt INTERFACE)
target_include_directories(entt INTERFACE third_party)

# Raylib
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
add_subdirectory(third_party/raylib)

# Core Library
add_library(Core
    src/Core/Logger.cpp
    src/Core/PAL.cpp
    src/Core/Memory.cpp
)

target_include_directories(Core PUBLIC src/Core)

# Pybind11 module
pybind11_add_module(velosia_core
    src/Engine/Bindings.cpp
    src/Engine/RenderSystem.cpp
)

target_link_libraries(velosia_core PRIVATE Core entt raylib)
