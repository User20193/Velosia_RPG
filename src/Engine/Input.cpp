#include "Input.hpp"
#include "DisplayManager.hpp"
#include <algorithm>

namespace Velosia::Engine {

    float Input::GetMouseX() {
        // Because of letterboxing, we need to map physical screen mouse coords
        // to the virtual internal canvas coords.
        float rawX = ::GetMouseX();
        float scale = std::min(
            (float)GetScreenWidth() / DisplayManager::GetInternalWidth(),
            (float)GetScreenHeight() / DisplayManager::GetInternalHeight()
        );

        float letterboxOffsetX = (GetScreenWidth() - (DisplayManager::GetInternalWidth() * scale)) * 0.5f;

        return (rawX - letterboxOffsetX) / scale;
    }

    float Input::GetMouseY() {
        float rawY = ::GetMouseY();
        float scale = std::min(
            (float)GetScreenWidth() / DisplayManager::GetInternalWidth(),
            (float)GetScreenHeight() / DisplayManager::GetInternalHeight()
        );

        float letterboxOffsetY = (GetScreenHeight() - (DisplayManager::GetInternalHeight() * scale)) * 0.5f;

        return (rawY - letterboxOffsetY) / scale;
    }

}
