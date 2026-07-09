cmake_minimum_required(VERSION 3.15)
project(VelosiaEngine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Build as a shared library for Python
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Find Python
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Use FetchContent for universal dependency management
include(FetchContent)

# Pybind11
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v3.0.0
)
FetchContent_MakeAvailable(pybind11)

# EnTT
FetchContent_Declare(
  entt
  GIT_REPOSITORY https://github.com/skypjack/entt.git
  GIT_TAG        v3.13.0
)
FetchContent_MakeAvailable(entt)

# We need to manually add EnTT include dirs since it might not expose a target correctly depending on the branch/version
include_directories(${entt_SOURCE_DIR}/single_include/entt)

# Raylib
set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
FetchContent_Declare(
  raylib
  GIT_REPOSITORY https://github.com/raysan5/raylib.git
  GIT_TAG        5.0
)
FetchContent_MakeAvailable(raylib)

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
    src/Engine/MovementSystem.cpp
    src/Engine/PlayerInputSystem.cpp
)

target_link_libraries(velosia_core PRIVATE Core EnTT::EnTT raylib)
