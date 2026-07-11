#include "Input.hpp"
#include "DisplayManager.hpp"
#include <algorithm>

namespace Velosia::Engine {

    float Input::GetMouseX() {
        // Because of letterboxing, we need to map physical screen mouse coords
        // to the virtual internal canvas coords.
        float rawX = ::GetMouseX();
        int internalWidth = DisplayManager::GetInternalWidth();
        int internalHeight = DisplayManager::GetInternalHeight();

        if (internalWidth <= 0 || internalHeight <= 0) return rawX;

        float scale = std::min(
            (float)GetScreenWidth() / internalWidth,
            (float)GetScreenHeight() / internalHeight
        );

        if (scale <= 0.0f) return rawX; // Prevent Division by Zero if window collapses

        float letterboxOffsetX = (GetScreenWidth() - (internalWidth * scale)) * 0.5f;

        return (rawX - letterboxOffsetX) / scale;
    }

    float Input::GetMouseY() {
        float rawY = ::GetMouseY();

        int internalWidth = DisplayManager::GetInternalWidth();
        int internalHeight = DisplayManager::GetInternalHeight();

        if (internalWidth <= 0 || internalHeight <= 0) return rawY;

        float scale = std::min(
            (float)GetScreenWidth() / internalWidth,
            (float)GetScreenHeight() / internalHeight
        );

        if (scale <= 0.0f) return rawY; // Prevent Division by Zero

        float letterboxOffsetY = (GetScreenHeight() - (internalHeight * scale)) * 0.5f;

        return (rawY - letterboxOffsetY) / scale;
    }

}
